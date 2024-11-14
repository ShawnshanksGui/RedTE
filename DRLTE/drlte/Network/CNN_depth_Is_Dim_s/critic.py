"""
    Critic of Deep Deterministic policy gradient

"""
import tflearn
import tensorflow as tf
import numpy as np

class CriticNetwork():
    def __init__(self, session, dim_state, dim_action, learning_rate, tau, num_actor_vars):
        self.__sess = session
        self.__dim_s = dim_state
        self.__dim_a = dim_action
        self.__learning_rate = learning_rate
        self.__tau = tau
        
        cur_para_num = len(tf.trainable_variables())
        self.__inputs, self.__action, self.__out = self.buildNetwork()
        self.__paras = tf.trainable_variables()[cur_para_num:]

        self.__target_inputs, self.__target_action, self.__target_out = self.buildNetwork()
        self.__target_paras = tf.trainable_variables()[(len(self.__paras) + cur_para_num):]

        self.__ops_update_target = []
        for i in range(len(self.__target_paras)):
            val = tf.add(tf.multiply(self.__paras[i], self.__tau), tf.multiply(self.__target_paras[i], 1. - self.__tau))
            op = self.__target_paras[i].assign(val)
            self.__ops_update_target.append(op)

        self.__q_predicted = tf.placeholder(tf.float32, [None, 1])
        self.__is_weight = tf.placeholder(tf.float32, [None, 1])

        self.loss = tflearn.mean_square(self.__q_predicted, self.__out)
        self.loss = tf.multiply(self.loss, self.__is_weight)
        self.optimize = tf.train.AdamOptimizer(self.__learning_rate).minimize(self.loss)

        self.__gradient_action = tf.gradients(self.__out, self.__action)
      

#CNN-based critic netowrk(depth of kernel = dim_state)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def myConv1d(self, input_1d, out_dim, my_filter_size, stride):
        input_2d = tf.expand_dims(input_1d, 1)
        print(input_2d.op.name, '', input_2d.get_shape().as_list())  
        #net = tf.layers.conv1d(input_2d, out_dim, my_filter_size, stride, padding='SAME', activation=tf.nn.relu)  
        net = tf.layers.conv1d(input_2d, out_dim, my_filter_size, stride, padding='SAME', activation=tf.nn.relu)          
        print(net.op.name, '', net.get_shape().as_list())        
        net = tf.squeeze(net, [1])          
#        print(net.op.name, '', net.get_shape().as_list())        
        print(net)                                         
        return net

    def buildNetwork(self):
        inputs = tf.placeholder(tf.float32, [None, self.__dim_s])
        action = tf.placeholder(tf.float32, [None, self.__dim_a])

        net = inputs      
        #net = self.myConv1d(net, self.__dim_s, [2], 1)         
        net = self.myConv1d(net, self.__dim_s, [4], 1)
        net = self.myConv1d(net, self.__dim_s, [2], 1)

        net = self.myConv1d(tf.concat([net, action], axis=1), self.__dim_s+self.__dim_a, [4], 1)         
       
        w_init = tflearn.initializations.uniform(minval=-3e-3, maxval=3e-3)
        out = tf.contrib.layers.fully_connected(net, 1, weights_initializer=w_init, activation_fn=None)

        print("inputs's original demension is:")
        print(inputs.get_shape().as_list())         
        
        print("action's original demension is:")
        print(action.get_shape().as_list())          
 
        print("out's original demension is:")
        print(out.get_shape().as_list())                        
                                        
        return inputs, action, out
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   

    def train(self, inputs, action, q_predicted, is_weight):
        return self.__sess.run([self.__out, self.optimize], feed_dict={
            self.__inputs: inputs,
            self.__action: action,
            self.__q_predicted: q_predicted,
            self.__is_weight: is_weight
        })

    def predict(self, inputs, action):
        return self.__sess.run(self.__out, feed_dict={
            self.__inputs: inputs,
            self.__action: action
        })

    def predict_target(self, inputs, action):
        return self.__sess.run(self.__target_out, feed_dict={
            self.__target_inputs: inputs,
            self.__target_action: action
        })

    def calculate_gradients(self, inputs, action):
        return self.__sess.run(self.__gradient_action, feed_dict={
            self.__inputs: inputs,
            self.__action: action
        })

    def update_target_paras(self):
        self.__sess.run(self.__ops_update_target)