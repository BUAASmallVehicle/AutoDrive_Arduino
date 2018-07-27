;; Auto-generated. Do not edit!


(when (boundp 'test_msg::test)
  (if (not (find-package "TEST_MSG"))
    (make-package "TEST_MSG"))
  (shadow 'test (find-package "TEST_MSG")))
(unless (find-package "TEST_MSG::TEST")
  (make-package "TEST_MSG::TEST"))

(in-package "ROS")
;;//! \htmlinclude test.msg.html


(defclass test_msg::test
  :super ros::object
  :slots (_test ))

(defmethod test_msg::test
  (:init
   (&key
    ((:test __test) 0)
    )
   (send-super :init)
   (setq _test (round __test))
   self)
  (:test
   (&optional __test)
   (if __test (setq _test __test)) _test)
  (:serialization-length
   ()
   (+
    ;; int16 _test
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _test
       (write-word _test s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _test
     (setq _test (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get test_msg::test :md5sum-) "0d3772b8a5da1299e56c0ae15e8afe56")
(setf (get test_msg::test :datatype-) "test_msg/test")
(setf (get test_msg::test :definition-)
      "int16 test

")



(provide :test_msg/test "0d3772b8a5da1299e56c0ae15e8afe56")


