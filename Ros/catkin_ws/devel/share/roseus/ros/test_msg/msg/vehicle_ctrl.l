;; Auto-generated. Do not edit!


(when (boundp 'test_msg::vehicle_ctrl)
  (if (not (find-package "TEST_MSG"))
    (make-package "TEST_MSG"))
  (shadow 'vehicle_ctrl (find-package "TEST_MSG")))
(unless (find-package "TEST_MSG::VEHICLE_CTRL")
  (make-package "TEST_MSG::VEHICLE_CTRL"))

(in-package "ROS")
;;//! \htmlinclude vehicle_ctrl.msg.html


(defclass test_msg::vehicle_ctrl
  :super ros::object
  :slots (_speed _accspeed _angle ))

(defmethod test_msg::vehicle_ctrl
  (:init
   (&key
    ((:speed __speed) 0.0)
    ((:accspeed __accspeed) 0.0)
    ((:angle __angle) 0.0)
    )
   (send-super :init)
   (setq _speed (float __speed))
   (setq _accspeed (float __accspeed))
   (setq _angle (float __angle))
   self)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:accspeed
   (&optional __accspeed)
   (if __accspeed (setq _accspeed __accspeed)) _accspeed)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:serialization-length
   ()
   (+
    ;; float32 _speed
    4
    ;; float32 _accspeed
    4
    ;; float32 _angle
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _accspeed
       (sys::poke _accspeed (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _speed
     (setq _speed (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _accspeed
     (setq _accspeed (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _angle
     (setq _angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get test_msg::vehicle_ctrl :md5sum-) "cb7f1353bf56e905646c8a5e041d332d")
(setf (get test_msg::vehicle_ctrl :datatype-) "test_msg/vehicle_ctrl")
(setf (get test_msg::vehicle_ctrl :definition-)
      "float32 speed
float32 accspeed
float32 angle

")



(provide :test_msg/vehicle_ctrl "cb7f1353bf56e905646c8a5e041d332d")


