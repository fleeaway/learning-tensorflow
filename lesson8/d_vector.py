import tensorflow as tf

# X = tf.placeholder(tf.float32, [None, 40])

def nn_layer(input, w_size, b_size, dropout=True):
    weight = tf.get_variable('weight', w_size, initializer=tf.random_normal_initializer())
    tf.summary.histogram(weight.name, weight)
    bias = tf.get_variable('bias', b_size, initializer=tf.random_normal_initializer())
    tf.summary.histogram(bias.name, bias)

    out = tf.add(tf.matmul(input, weight), bias)
    tf.summary.histogram("liear_out", out)
    out = tf.nn.relu(out)
    return tf.nn.dropout(out, 0.5) if dropout else out


def d_vector_model(input):
    with tf.variable_scope("layer1") as layer1_score:
        layer1 = nn_layer(input, [40, 256], [256], dropout=False)
        tf.summary.histogram('layer1_output', layer1)
    with tf.variable_scope("layer2") as layer2_score:
        layer2 = nn_layer(layer1, [256, 256], [256], dropout=False)
        tf.summary.histogram('layer2_output', layer2)
    with tf.variable_scope("layer3") as layer3_score:
        layer3 = nn_layer(layer2, [256, 256], [256])
        tf.summary.histogram('layer3_output', layer3)
    with tf.variable_scope("layer4") as layer4_score:
        out = nn_layer(layer3, [256, 256], [256])
        tf.summary.histogram('layer4_output', out)
    return out

# d_vector = d_vector_model(X)

# def train():
#     batch_num = dp.train_data.shape[0] // BATCH_SIZE + dp.train_data.shape[0] % BATCH_SIZE
#     label_num = dp.train_label.shape[1]
#     generator = dp.generate_batch(BATCH_SIZE)

#     global_step = tf.Variable(0, trainable=False)
#     Y = tf.placeholder(tf.float32, [None, label_num])

#     def loss_func(d_vector, y):
#         with tf.variable_scope("predict") as predict_layer:
#             predict = nn_layer(d_vector, [256, label_num], [label_num], dropout=False)
#         return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predict, labels=y))

#     loss_function = loss_func(d_vector, Y)
#     learning_rate = tf.train.exponential_decay(1e-3, global_step, 50000, 0.1, staircase=True)
#     optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss_function, global_step=global_step)

#     saver = tf.train.Saver()
#     with tf.Session() as session:
#         session.run(tf.global_variables_initializer())    
#         writer = tf.summary.FileWriter('logs/', session.graph)

#         if not os.path.exists(model_dir):
#             os.mkdir(model_dir)

#         i = 0
#         while i < epoch:

#             for batch in range(batch_num):
#                 data, label = next(generator)
#                 # print(data)
#                 # print(label)
#                 _, l, lr, gs = session.run([optimizer, loss_function, learning_rate, global_step], feed_dict={X: data, Y: label})
#                 print(l, lr, gs)

#                 if gs % 5000 == 0:
#                     saver.save(session, model_dir + 'd_vector.module', global_step=gs)

#             i += 1
#             saver.save(session, model_dir + 'd_vector.module_%d' % i)
#             # eval the test set

# if __name__ == '__main__':
#     train()