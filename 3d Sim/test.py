import numpy as np
from ThreeD import ThreeD
print('here')
import quaternion as quat
print('here')
import math

print('here')
curr_vect = ThreeD(10.0,1.0,1.0)
old_vect  = ThreeD(-10.0, -5.0, -3.0)
axis = curr_vect.cross(old_vect)

dot = curr_vect.dot(old_vect)
theta = math.acos(dot/(curr_vect.mag() * old_vect.mag()))
print('current angle between vectors'+ str(theta))
threshold = np.deg2rad(50)
print('Threshold:' + str(threshold) )

theta = (theta - threshold)

vector = np.array([0.] + list(curr_vect))
rot_axis = np.array([0.] + list(axis))
axis_angle = (theta * .5) * rot_axis/np.linalg.norm(rot_axis)

#Create the quaternions qvec and qlog using the library and get the unit roatation quaternion q by taking the exponential
qvec = quat.quaternion(*vector)
qlog = quat.quaternion(*axis_angle)
q = np.exp(qlog)

#Finally we calculate the rotation of the vector by the following operation
#v_prime = q * qvec * np.conjugate(q)
v_prime = q * qvec * quat.quaternion(q.real, *(-q.imag))

final_v = v_prime.imag
print(final_v)

final_vector = ThreeD(final_v[0], final_v[1], final_v[2])
dot = final_vector.dot(old_vect)
angle = math.acos(dot/(final_vector.mag() * old_vect.mag()))
print(angle)
