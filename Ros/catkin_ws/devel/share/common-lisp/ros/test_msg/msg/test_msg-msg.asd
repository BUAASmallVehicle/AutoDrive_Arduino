
(cl:in-package :asdf)

(defsystem "test_msg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "test" :depends-on ("_package_test"))
    (:file "_package_test" :depends-on ("_package"))
    (:file "vehicle_ctrl" :depends-on ("_package_vehicle_ctrl"))
    (:file "_package_vehicle_ctrl" :depends-on ("_package"))
  ))