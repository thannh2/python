import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn import linear_model
import matplotlib.animation as animation


def cost(x):
	m = A.shape[0]
	return 0.5/m * np.linalg.norm(A.dot(x) - b, 2)**2

def grad(x):
	m = A.shape[0]
	return 1/m * A.T.dot(A.dot(x) - b)

def gradient_descent(x_init, learning_rate, iteration):
	x_list = [x_init]
	for i in range(iteration):
		x_init = x_init - learning_rate*grad(x_init)
		x_list.append(x_init)
	return x_list

def check_grad(x):
	eps = 1e-4
	g = np.zeros_like(x)
	for i in range(len(x)):
		x1 = x.copy()
		x2 = x.copy()
		x1[i] += eps
		x2[i] -= eps
		g[i] = (cost(x1) - cost(x2))/(2*eps)

	g_grad = grad(x)
	if np.linalg.norm(g - g_grad) > 1e-7:
		print("Wraning")
#x_list tuong ung voi a, b trong y = ax + b

#Data
A = np.array([[2, 5, 7, 9, 11, 16, 19, 23, 22, 29, 29, 35, 37, 40, 46]]).T
b = np.array([[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]).T

#Draw Data
fig1 = plt.figure("GD for linear regression")
ax = plt.axes(xlim=(-10,60), ylim=(-1,20))
plt.plot(A, b, 'ro')

#linear regression draw
lr = linear_model.LinearRegression()
lr.fit(A,b)
x0_gd = np.linspace(1, 46, 2)
y0_linear = lr.intercept_[0] + lr.coef_[0][0] * x0_gd

plt.plot(x0_gd, y0_linear, color = "green")

#
ones = np.ones((A.shape[0] , 1), dtype = np.int8)
A = np.concatenate((ones, A), axis = 1)
#random initial line
x_init = np.array([[1.0],[2.0]])

#gradient descent data
iteration = 100
learning_rate = 0.0001
x_list = gradient_descent(x_init, learning_rate, iteration)
print(x_list)
#draw animation
line , = ax.plot([],[], color = "blue")
def update(i):
	y0_gd = x_list[i][0]+ x_list[i][1] * x0_gd
	line.set_data(x0_gd, y0_gd)
	return line ,

iters = np.arange(1, len(x_list), 1)
line_animation = animation.FuncAnimation(fig1, update, iters, interval = 50, blit = True)

#legend for plot
plt.legend(('Value in each GD iteration', 'Solution by formular', 'Inital value for GD'), loc = (0.52, 0.01))
ltext = plt.gca().get_legend().get_texts()

for i in range(len(x_list)):
	y0_x_list = x_list[i][0] + x_list[i][1] * x0_gd
	plt.plot(x0_gd, y0_x_list, color = "black", alpha = 0.3)

# y0_x_list = x_list[-1][0] + x_list[-1][1] * x0_gd
# plt.plot(x0_gd, y0_x_list, color = "red")
plt.show()