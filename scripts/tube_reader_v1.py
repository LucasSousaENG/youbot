#Ref: https://github.com/thecalmguy/Line-Following-drone

from logging import captureWarnings
import rospy
import cv2
import numpy as np
import math
import time
from geometry_msgs.msg import Twist, PoseStamped
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from sensor_msgs.msg import Image
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

#Class that initiates the Gstreamer image pipeline  
class Video():
    """BlueRov video capture class constructor
    Attributes:
        port (int): Video UDP port
        video_codec (string): Source h264 parser
        video_decode (string): Transform YUV (12bits) to BGR (24bits)
        video_pipe (object): GStreamer top-level pipeline
        video_sink (object): Gstreamer sink element
        video_sink_conf (string): Sink configuration
        video_source (string): Udp source ip and port
    """

    def __init__(self, port=5600):
        """Summary
        Args:
            port (int, optional): UDP port
        """

        Gst.init(None)

        self.port = port
        self._frame = None

        # [Software component diagram](https://www.ardusub.com/software/components.html)
        # UDP video stream (:5600)
        self.video_source = 'udpsrc port={}'.format(self.port)
        # [Rasp raw image](http://picamera.readthedocs.io/en/release-0.7/recipes2.html#raw-image-capture-yuv-format)
        # Cam -> CSI-2 -> H264 Raw (YUV 4-4-4 (12bits) I420)
        self.video_codec = '! application/x-rtp, payload=96 ! rtph264depay ! h264parse ! avdec_h264'
        # Python don't have nibble, convert YUV nibbles (4-4-4) to OpenCV standard BGR bytes (8-8-8)
        self.video_decode = \
            '! decodebin ! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert'
        # Create a sink to get data
        self.video_sink_conf = \
            '! appsink emit-signals=true sync=false max-buffers=2 drop=true'

        self.video_pipe = None
        self.video_sink = None

        self.run()

    def start_gst(self, config=None):
        """ Start gstreamer pipeline and sink
        Pipeline description list e.g:
            [
                'videotestsrc ! decodebin', \
                '! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert',
                '! appsink'
            ]
        Args:
            config (list, optional): Gstreamer pileline description list
        """

        if not config:
            config = \
                [
                    'videotestsrc ! decodebin',
                    '! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert',
                    '! appsink'
                ]

        command = ' '.join(config)
        self.video_pipe = Gst.parse_launch(command)
        self.video_pipe.set_state(Gst.State.PLAYING)
        self.video_sink = self.video_pipe.get_by_name('appsink0')

    @staticmethod
    def gst_to_opencv(sample):
        """Transform byte array into np array
        Args:
            sample (TYPE): Description
        Returns:
            TYPE: Description
        """
        buf = sample.get_buffer()
        caps = sample.get_caps()
        array = np.ndarray(
            (
                caps.get_structure(0).get_value('height'),
                caps.get_structure(0).get_value('width'),
                3
            ),
            buffer=buf.extract_dup(0, buf.get_size()), dtype=np.uint8)
        return array

    def frame(self):
        """ Get Frame
        Returns:
            iterable: bool and image frame, cap.read() output
        """
        return self._frame

    def frame_available(self):
        """Check if frame is available
        Returns:
            bool: true if frame is available
        """
        return type(self._frame) != type(None)

    def run(self):
        """ Get frame to update _frame
        """

        self.start_gst(
            [
                self.video_source,
                self.video_codec,
                self.video_decode,
                self.video_sink_conf
            ])

        self.video_sink.connect('new-sample', self.callback)

    def callback(self, sink):
        sample = sink.emit('pull-sample')
        new_frame = self.gst_to_opencv(sample)
        self._frame = new_frame

        return Gst.FlowReturn.OK
#End of Class Video that initiates the Gstreamer



#This a simple callback func will save the current state of the autopilot/px4/Drone
current_state = State()
def state_cb(msg): 
    global current_state
    current_state = msg

    # position callback function will fill the local_pos message with current position of drone
local_pos = PoseStamped()
def posCb(msg):
    global local_pos
    local_pos.pose.position.x = msg.pose.position.x
    local_pos.pose.position.y = msg.pose.position.y
    local_pos.pose.position.z = msg.pose.position.z

global alt_def
global y_def
alt_def = 3
y_def = 0
# message to hold the counter-clockw part that cause problem. label must be an integer, It doesnt accept strin
def main_func():
    counter = 0
    # initializing a node to communicate with the ROS Master
    rospy.init_node("line_follower_node")  
    
    #getting (subscribing) the PX4 status
    state_sub = rospy.Subscriber("mavros/state", State, callback = state_cb,  queue_size=10)
    
    # initializing a velocity publisher, to publish velocity on the cmd_vel topic
    vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=10)
    
    # initializing a position setpoint publisher, to publish position setpoint on the setpoint_raw/local topic
    sp_pub = rospy.Publisher("mavros/setpoint_position/local", PoseStamped, queue_size=10)

    #[NOT IN USE YET] setting gimbal
    gimbal_pos_pub = rospy.Publisher('mavros/mount_control/command', MountControl, queue_size = 10)

    #arming the drone
    rospy.wait_for_service("/mavros/cmd/arming")
    arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)    

    #receiving the set mode
    rospy.wait_for_service("/mavros/set_mode")
    set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)
    
    # subscribing to the local_position/pose topic to get the current location
    rospy.Subscriber('mavros/local_position/pose', PoseStamped, posCb)
    
    # Setpoint publishing MUST be faster than 2Hz. PX4 has a timeout of 500ms between two OFFBOARD commands
    rate = rospy.Rate(20.0)
    
    # Wait for Flight Controller connection
    while(not rospy.is_shutdown() and not current_state.connected):
        print("Trying to connect...")
        rate.sleep()
    
    # [NOT IN USE YET] This func defines a static position  for the gimbal
    gb_control = MountControl()
    gb_control.header.stamp = rospy.Time.now()
    gb_control.header.frame_id = "map"
    gb_control.mode = 2        
    gb_control.roll = 0
    gb_control.pitch = -60
    gb_control.yaw = 0
    
    #definig te pos_hold var, setpoint of position
    pos_hold = PoseStamped()
    #linear position x, y and z
    pos_hold.pose.position.x = 2
    pos_hold.pose.position.y = y_def
    pos_hold.pose.position.z = alt_def
    #angular position pitch, roll and yaw
    pos_hold.pose.orientation.w = 0
    pos_hold.pose.orientation.x = 0
    pos_hold.pose.orientation.y = 0
    pos_hold.pose.orientation.z = 0 #yaw

    # message to hold the forward velocity that we want to give to the drone
    # publishing this message will give the drone a forward velocity
    fwd_vel = Twist()
    fwd_vel.linear.x = 0.5
    fwd_vel.linear.y = 0
    fwd_vel.linear.z = 0

    # message to hold the left translational velocity that we want to give to the drone
    left_vel = Twist()
    left_vel.linear.x = 0
    left_vel.linear.y = -0.5
    left_vel.linear.z = 0

    # message to hold the right translational velocity that we want to give to the drone
    right_vel = Twist()
    right_vel.linear.x = 0
    right_vel.linear.y = 0.5
    right_vel.linear.z = 0
    # message to hold the right translational velocity that we want to give to the drone
    up_vel = Twist()
    up_vel.linear.x = 0
    up_vel.linear.y = 0
    up_vel.linear.z = 0.5

    # message to hold the clockwise yaw velocity that we want to give to the drone
    cw_yaw = Twist()
    cw_yaw.angular.x = 0
    cw_yaw.angular.y = 0
    cw_yaw.angular.z = 0




    # Send a few setpoints before starting. Before entering OFFBOARD mode, you must have already started streaming setpoints. Otherwise the mode switch will be rejected. Below, 100 was chosen as an arbitrary amount.
    for i in range(100):   
        if(rospy.is_shutdown()):
            print(".")
            break
        print("Pose publishing")
        sp_pub.publish(pos_hold)
        gimbal_pos_pub.publish(gb_control)
        rate.sleep()

    offb_set_mode = SetModeRequest()
    offb_set_mode.custom_mode = 'OFFBOARD'

    arm_cmd = CommandBoolRequest()
    arm_cmd.value = True

    last_req = rospy.Time.now()
    
    alt_sp = np.array((2, y_def, alt_def))
    alt_offset = 2
    checkpoint1 = False
    ang = 10 #recem criado
    ang_offset = 2
    x_offset = 200
    y_offset = 50
    x1old = 0
    x2old = 0
    error_x = 10 #recem criado
    
    contRef = 0
    #Initializing Gstreamer
    video = Video()

    while(not rospy.is_shutdown()):

        if not video.frame_available():
            continue

        if(current_state.mode != "OFFBOARD" and (rospy.Time.now() - last_req) > rospy.Duration(5.0)):
            print("It's not running in offboard mode yet...")
            if(set_mode_client.call(offb_set_mode).mode_sent == True):
                rospy.loginfo("OFFBOARD enabled")
            
            last_req = rospy.Time.now()
        else:
            if(not current_state.armed and (rospy.Time.now() - last_req) > rospy.Duration(5.0)):
                if(arming_client.call(arm_cmd).success == True):
                    rospy.loginfo("Vehicle armed")
            
                last_req = rospy.Time.now()

        sp_pub.publish(pos_hold)
        gimbal_pos_pub.publish(gb_control)
        if (contRef == 0):
            print("Pose Var: ", pos_hold)
            print("Gimbal Pose: ", gb_control)
            contRef = contRef + 1
        
        # setting threshholds for the defective frames that we got from defective_frame.py
        if ((counter >= 73) and (counter <= 82)):
            thresh_min = 60
            thresh_max = 70
        elif ((counter >= 83) and (counter <= 86)):
            thresh_min = 50
            thresh_max = 60
        elif ((counter >= 86) and (counter <= 92)):
            thresh_min = 60
            thresh_max = 70
        elif ((counter >= 110) and (counter <= 112)):
            thresh_min = 30
            thresh_max = 50
        else:
            thresh_min = 20
            thresh_max = 25
        
        pos = np.array((local_pos.pose.position.x, local_pos.pose.position.y, local_pos.pose.position.z))

        if np.linalg.norm(alt_sp - pos) < alt_offset:
            checkpoint1 = True
        if checkpoint1 == False:
            sp_pub.publish(pos_hold)
        if checkpoint1 == True:
            print("Checkpoint1!")
            # Capture frame-by-frame
            frame = video.frame()
            #frame = cv2.resize(frame, (320, 360))      #L A 
            # solucao temporaria para lading gear issue
            # Cropping an image
            #frame = frame[20:280, 58:260]
            height = frame.shape[0]
            width = frame.shape[1]  
            print("height: ",height)
            print("width: ",width)   
            cv2.imshow('frame', frame)
            
            #Image gray scale convertion
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #Other filters that might help
            kernel2 = np.ones((17,17),np.uint8)
            erosion = cv2.dilate(gray,kernel2,iterations = 1)

            #Apply Edge Detection method on the image
            edges = cv2.Canny(erosion,thresh_min,thresh_max,apertureSize = 3)
            #Image Binarization 
            ret,thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            #Showing the imgae binarized and the edge applied after the binarization
            cv2.imshow("Binary Image", thresh)
            cv2.imshow("Canny Detection", edges)
            
            # This returns an array of r and theta values
            lines = cv2.HoughLines(edges,1,np.pi/180, 100)
            
            if lines is not None:
                #print("Entrei no if de lines")
                for r,theta in lines[0]:
                    print('check')
                
                # Stores the value of cos(theta) in a
                    a = np.cos(theta)

                # Stores the value of sin(theta) in b
                    b = np.sin(theta)

                # x0 stores the value rcos(theta)
                    x0 = a*r

                # y0 stores the value rsin(theta)
                    y0 = b*r

                # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
                    x1 = int(x0 + 1000*(-b))

                # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
                    y1 = int(y0 + 1000*(a))

                # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
                    x2 = int(x0 - 1000*(-b))

                # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
                    y2 = int(y0 - 1000*(a))
                    center_x = (x1+x2)/2
                    center_y = (y1+y2)/2
                    error_x = center_x - 180
                    if (x2 - x1 == 0):
                        ang = 0
                    else:
                        ang = -1*(math.atan((y2 - y1)/(x2 -x1)))

            # etapa de ajuste de leitura (o trabalho atual trata de somar as distancias novas e antigas e dividir por 2 para encontrar o meio termo entre as leituras e evitar ficar "sambando"
            #Ainda assim, a leitura esta errada. Portanto o ideal e identificar o problema na leitura
		
                    print("A diferenca entre o x1 atual e o antigo:" + str(x1-x1old))
                    print("A diferenca entre o x2 atual e o antigo:" + str(x2-x2old))
                    x1 = (x1+x1old)/2
                    x2 = (x2+x2old)/2
                    x1old = x1
                    x2old = x2  
                    print("\n")

                    # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
                    # (0,0,255) denotes the colour of the line to be
                    #drawn. In this case, it is red.
                    ang = round(ang, 2)
                    cv2.line(frame,(x1,y1), (x2,y2), (0,0,255),5)
                    #right blue ref line 
                    #cv2.line(frame,(160 + x_offset,0), (160 + x_offset,360), (255,0,0), 2) #usar como referencia para realizar curvas e se autoconsertar
                    #left blue ref line
                    #cv2.line(frame,(160 - x_offset,0), (160 - x_offset,360), (255,0,0), 2)
                    #upper blue ref line
                    #cv2.line(frame,(0, 100 - y_offset), (360,100 - y_offset), (255,0,0), 2)
                    #upper green text
                    #cv2.putText(frame, str(ang), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    #Lowest green text
                    #cv2.putText(frame, str(error_x), (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Display the resulting frame
                cv2.imshow('Hough Transform Detection',frame)
                print("frame processed, angle:", ang)
                print("error x: ", error_x)

        if np.linalg.norm(alt_sp[2] - float(pos[2])) < alt_offset:
            vel_pub.publish(up_vel)
        if abs(ang) < ang_offset:
            if ang > 0:
                cw_yaw.angular.z = 1
                vel_pub.publish(cw_yaw)
                print("Clockwise...  ")
		    #time.sleep(0.5)
            if ang < 0:
                cw_yaw.angular.z = -1
                vel_pub.publish(cw_yaw)
                print("Anti Clockwise...  ")
		     #time.sleep(0.5)
            if abs(ang) > ang_offset:

                if abs(error_x) > x_offset:
                    if error_x > 0:
                        vel_pub.publish(left_vel)
                        print("Left...  ")

                    if error_x < 0:
                        vel_pub.publish(right_vel)
                        print("Right...  ")

        if (abs(ang) < ang_offset and abs(error_x) < x_offset):

            vel_pub.publish(fwd_vel)
            print("Forward...  ")

        # Press Q on keyboard to  exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #cv2.imwrite("defective frame.jpg", frame)
            break
        counter += 1

        rate.sleep()
        #time.sleep(0.3)

    # Closes all the frames
    cv2.destroyAllWindows()   

if __name__ == '__main__':
    try:
        main_func()
    except rospy.ROSInterruptException:
        pass
