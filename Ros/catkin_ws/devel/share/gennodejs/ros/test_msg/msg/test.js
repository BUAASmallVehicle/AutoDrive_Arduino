// Auto-generated. Do not edit!

// (in-package test_msg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class test {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.test = null;
    }
    else {
      if (initObj.hasOwnProperty('test')) {
        this.test = initObj.test
      }
      else {
        this.test = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type test
    // Serialize message field [test]
    bufferOffset = _serializer.int16(obj.test, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type test
    let len;
    let data = new test(null);
    // Deserialize message field [test]
    data.test = _deserializer.int16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 2;
  }

  static datatype() {
    // Returns string type for a message object
    return 'test_msg/test';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0d3772b8a5da1299e56c0ae15e8afe56';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int16 test
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new test(null);
    if (msg.test !== undefined) {
      resolved.test = msg.test;
    }
    else {
      resolved.test = 0
    }

    return resolved;
    }
};

module.exports = test;
