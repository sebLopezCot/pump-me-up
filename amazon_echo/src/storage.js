/**
    Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.amazon.com/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

'use strict';
var AWS = require("aws-sdk");

var storage = (function () {
    var dynamodb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

    /*
     * The User class stores all user states
     */
    function User(session, data) {
        if (data) {
            this.data = data;
        } else {
            this.data = {
                awakeness: "50.0",
                out_of_frame: true,
                should_flash: false
            };
        }
        this._session = session;
    }

    User.prototype = {
        updateDB: function(callback){
            this._session.attributes.currentUser = this.data;
            dynamodb.putItem({
                TableName: 'users',
                Item: {
                    CustomerId: {
                        S: this._session.user.userId
                    },
                    Data: {
                        S: JSON.stringify(this.data)
                    }
                }
            }, function (err, data) {
                if (err) {
                    console.log(err, err.stack);
                }
                if (callback) {
                    callback();
                }
            });
        },
        updateFlash: function(state) {
            var userData = this.data;
            userData.should_flash = true;
        },
        getAwakeness: function(){
            var userData = this.data;
            return userData.awakeness;
        },
        isOutOfFrame: function () {
            // check if the user is out of the frame
            var userData = this.data;
            return userData.out_of_frame;
        },
    };

    return {
        loadUser: function (session, callback) {
            if (session.attributes.currentUser) {
                console.log('get user from session=' + session.attributes.currentUser);
                callback(new User(session, session.attributes.currentUser));
                return;
            }
            dynamodb.getItem({
                TableName: 'users',
                Key: {
                    CustomerId: {
                        S: session.user.userId
                    }
                }
            }, function (err, data) {
                var currentUser;
                if (err) {
                    console.log(err, err.stack);
                    currentUser = new User(session);
                    session.attributes.currentUser = currentUser.data;
                    callback(currentUser);
                } else if (data.Item === undefined) {
                    currentUser = new currentUser(session);
                    session.attributes.currentUser = currentUser.data;
                    callback(currentUser);
                } else {
                    console.log('get user from dynamodb=' + data.Item.Data.S);
                    currentUser = new User(session, JSON.parse(data.Item.Data.S));
                    session.attributes.currentUser = currentUser.data;
                    callback(currentUser);
                }
            });
        },
        newUser: function (session) {
            return new User(session);
        }
    };
})();
module.exports = storage;
