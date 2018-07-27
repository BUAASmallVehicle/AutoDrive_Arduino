; Auto-generated. Do not edit!


(cl:in-package test_msg-msg)


;//! \htmlinclude vehicle_ctrl.msg.html

(cl:defclass <vehicle_ctrl> (roslisp-msg-protocol:ros-message)
  ((speed
    :reader speed
    :initarg :speed
    :type cl:float
    :initform 0.0)
   (accspeed
    :reader accspeed
    :initarg :accspeed
    :type cl:float
    :initform 0.0)
   (angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0))
)

(cl:defclass vehicle_ctrl (<vehicle_ctrl>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <vehicle_ctrl>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'vehicle_ctrl)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name test_msg-msg:<vehicle_ctrl> is deprecated: use test_msg-msg:vehicle_ctrl instead.")))

(cl:ensure-generic-function 'speed-val :lambda-list '(m))
(cl:defmethod speed-val ((m <vehicle_ctrl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader test_msg-msg:speed-val is deprecated.  Use test_msg-msg:speed instead.")
  (speed m))

(cl:ensure-generic-function 'accspeed-val :lambda-list '(m))
(cl:defmethod accspeed-val ((m <vehicle_ctrl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader test_msg-msg:accspeed-val is deprecated.  Use test_msg-msg:accspeed instead.")
  (accspeed m))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <vehicle_ctrl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader test_msg-msg:angle-val is deprecated.  Use test_msg-msg:angle instead.")
  (angle m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <vehicle_ctrl>) ostream)
  "Serializes a message object of type '<vehicle_ctrl>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'speed))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'accspeed))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <vehicle_ctrl>) istream)
  "Deserializes a message object of type '<vehicle_ctrl>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'speed) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'accspeed) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<vehicle_ctrl>)))
  "Returns string type for a message object of type '<vehicle_ctrl>"
  "test_msg/vehicle_ctrl")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'vehicle_ctrl)))
  "Returns string type for a message object of type 'vehicle_ctrl"
  "test_msg/vehicle_ctrl")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<vehicle_ctrl>)))
  "Returns md5sum for a message object of type '<vehicle_ctrl>"
  "cb7f1353bf56e905646c8a5e041d332d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'vehicle_ctrl)))
  "Returns md5sum for a message object of type 'vehicle_ctrl"
  "cb7f1353bf56e905646c8a5e041d332d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<vehicle_ctrl>)))
  "Returns full string definition for message of type '<vehicle_ctrl>"
  (cl:format cl:nil "float32 speed~%float32 accspeed~%float32 angle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'vehicle_ctrl)))
  "Returns full string definition for message of type 'vehicle_ctrl"
  (cl:format cl:nil "float32 speed~%float32 accspeed~%float32 angle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <vehicle_ctrl>))
  (cl:+ 0
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <vehicle_ctrl>))
  "Converts a ROS message object to a list"
  (cl:list 'vehicle_ctrl
    (cl:cons ':speed (speed msg))
    (cl:cons ':accspeed (accspeed msg))
    (cl:cons ':angle (angle msg))
))
