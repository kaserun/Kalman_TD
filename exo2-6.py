# https://www.ensta-bretagne.fr/jaulin/robmooc.html
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def draw_room():
    for j in range(A.shape[1]):
        plot(array([A[0, j], B[0, j]]), array([A[1, j], B[1, j]]), color='blue')


def draw(p, y, col):
    draw_tank(p, 'darkblue', 0.1)
    p = p.flatten()
    y = y.flatten()
    for i in arange(0, 8):
        if i==0:
            color = 'red'
        else:
            color = col
        plot(p[0] + array([0, y[i] * cos(p[2] + i * pi / 4)]), p[1] + array([0, y[i] * sin(p[2] + i * pi / 4)]),
             color=color)


A = array([[0, 7, 7, 9, 9, 7, 7, 4, 2, 0, 5, 6, 6, 5],
           [0, 0, 2, 2, 4, 4, 7, 7, 5, 5, 2, 2, 3, 3]])
B = array([[7, 7, 9, 9, 7, 7, 4, 2, 0, 0, 6, 6, 5, 5],
           [0, 2, 2, 4, 4, 7, 7, 5, 5, 0, 2, 3, 3, 2]])
y = array([[6.4], [3.6], [2.3], [2.1], [1.7], [1.6], [3.0], [3.1]])
x_max = max(A[0])
y_max = max(A[1])


def f(p):
    y = 10000 * np.ones(8)
    m = np.array([p[0, 0], p[1, 0]])
    for j in range(8):
        u = np.array([cos(p[2, 0] + j * pi / 4), sin(p[2, 0] + j * pi / 4)])
        for i in range(len(A[0])):
            a = np.array([A[0,i], A[1, i]])
            b = np.array([B[0,i], B[1, i]])
            M_am_u = np.array([[a[0] - m[0], u[0]], [a[1] - m[1], u[1]]])
            M_bm_u = np.array([[b[0] - m[0], u[0]], [b[1] - m[1], u[1]]])
            M_am_ba = np.array([[a[0] - m[0], b[0] - a[0]], [a[1] - m[1], b[1] - a[1]]])
            M_u_ba = np.array([[u[0], b[0] - a[0]], [u[1], b[1] - a[1]]])
            if det(M_am_u) * det(M_bm_u) <= 0 and det(M_am_ba) * det(M_u_ba) >= 0 and det(M_u_ba) != 0:
                d_j_i = det(M_am_ba) / det(M_u_ba)
                y[j] = min(y[j], d_j_i)
    return y

def j_diff(p_chap, y):
    y_vect = y.flatten()
    y_estim = f(p_chap)
    return np.linalg.norm(y_estim - y_vect)

def global_simulated_annealing(y):
    n = 2
    x_decoup = linspace(0, x_max, n)
    y_decoup = linspace(0, y_max, n)
    theta_decoup = linspace(0, 2 * pi, n)
    epsilon = 0.5
    list_p_chap = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                p_chap = np.array([[x_decoup[i]], [y_decoup[j]], [theta_decoup[k]]])
                draw(p_chap, y, 'black')
                x_borne, y_borne, theta_borne = min(j_diff(p_chap, y), x_max), min(j_diff(p_chap, y), y_max), 2 * np.pi
                while (j_diff(p_chap, y) > epsilon):
                    d_rand = rand(3)
                    d_rand[0] = 2 * x_borne * d_rand[0] - x_borne
                    d_rand[1] = 2 * y_borne * d_rand[1] - y_borne
                    d_rand[2] = 2 * theta_borne * d_rand[2] - theta_borne
                    q_chap = np.array([[p_chap[0, 0] + d_rand[0]], [p_chap[1, 0] + d_rand[1]], [p_chap[2, 0] + d_rand[2]]])
                    dist_p_chap = j_diff(p_chap, y)
                    dist_q_chap = j_diff(q_chap, y)
                    print('--------------------------------')
                    print('p_chap =', p_chap)
                    print('q_chap =', q_chap)
                    print('dist_p_chap =', dist_p_chap)
                    print('dist_q_chap =', dist_q_chap)
                    print('x_borne = {}, y_borne = {}, theta_borne = {}'.format(x_borne, y_borne, theta_borne))
                    if dist_q_chap < dist_p_chap:
                        p_chap = q_chap
                        x_borne = min(0.75 * x_borne, dist_p_chap)
                        y_borne = min(.75 * y_borne, dist_p_chap)
                        theta_borne = min(.75*t)
                        print('Update p_chap')
                draw(p_chap, y, 'green')
                list_p_chap.append(p_chap)
    return list_p_chap

def local_simulated_annealing(y):
    p_chap = rand(3, 1)
    epsilon = .1
    dist_p_chap = j_diff(p_chap, y)
    x_borne = min(x_max, dist_p_chap)
    y_borne = min(y_max, dist_p_chap)
    theta_borne = 2 * pi
    p_chap[0,0] *= x_borne
    p_chap[1,0] *= y_borne
    p_chap[2,0] *= theta_borne
    dist_p_chap = j_diff(p_chap, y)
    while dist_p_chap > epsilon and x_borne > epsilon/10 and y_borne > epsilon/10:
        d = rand(3,1)
        d[0,0] = 2*x_borne*d[0,0]-x_borne
        d[1,0] = 2*y_borne*d[1,0]-y_borne
        d[2,0] = 2*theta_borne*d[2,0]-theta_borne
        q_chap = p_chap + d
        dist_q_chap = j_diff(q_chap, y)
        print('--------------------------------')
        print('p_chap =', p_chap)
        print('q_chap =', q_chap)
        print('dist_p_chap =', dist_p_chap)
        print('dist_q_chap =', dist_q_chap)
        if dist_q_chap < dist_p_chap:
            p_chap = q_chap
            dist_p_chap = dist_q_chap
            x_borne = min(.9*x_borne, 1.5*dist_p_chap)
            y_borne = min(.9*y_borne, 1.5*dist_p_chap)
            theta_borne = min(.9*theta_borne, 1.5*dist_p_chap)
            print('Update p_chap')
            draw(p_chap, y, 'black')
        print('x_borne =', x_borne)
        print('y_borne =', y_borne)
        print('theta_borne =', theta_borne)
        pause(0.01)
    draw(p_chap, y, 'green')






ax = init_figure(-2, 10, -2, 10)
p0 = np.array([[1], [2], [3]]) #initial guess
draw_room()
# global_simulated_annealing(y)
local_simulated_annealing(y)
pause(10)