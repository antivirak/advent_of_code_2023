import numpy as np

# tohle nebude vubec easy, kazdy casovy okamzik se meni pozice a
# nikdy nemusi byt v jedne rade, protoze se s nimi proste musim po ceste srazit
# a ja mam taky jen pocatecni pos a vel.
# Mohla by to byt nejakym zpusobem optimalizacni uloha.
# zacnem na nahodne pozici a budem upravovat.
# Co bude ale ucelova funkce?
# pocatecni norma rychlosti by mohla bejt neco jako prumerna vzdalenost mezi kroupami


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        vectors = f_in.readlines()

    pos = []
    vel = []
    for vector in vectors:
        pos_str, vel_str = vector.strip().split(' @ ')
        pos.append(list(map(int, pos_str.split(', '))))
        vel.append(list(map(int, vel_str.split(', '))))

    # Translate into the frame of reference of the first hailstone, in other words,
    # subtract the position and velocity of the first hailstone from all of them. So in this frame,
    # the rock must go through the origin at some time.

    # The path of the second hailstorm forms a line. The rock must also intersect this line.
    # That means, the rock must be in the plane formed by that line and the origin.
    # Find when and where hailstones 3 & 4 intersect the plane.
    # That gives the position and velocity of the rock at two different times, which determines the entire trajectory of the rock.
    # So you only need 4 hailstones to determine the answer.

    # make all positions and velocities relative to the first hailstone
    pos = np.array(pos)
    vel = np.array(vel) - vel[0]
    # define the plane using the second hailstone. Use the [0, 0, 0] and 2 points in 2nd hailstone's trajectory
    points = [pos[1] + vel[1] * step for step in range(2)]
    # ax + by + cz + d = 0
    # print(points)
    n = np.cross(points[0] - pos[0], points[1] - pos[0])  # normal vector of the plane
    d = -np.dot(n, pos[1])  # d = -ax - by - cz
    print(d)
    # print(n)
    # find when and where hailstones 3 & 4 intersect the plane
    # parametric equation of a line for hailstone 3 trajectory
    # pos3 + vel3 * t
    # pos4 + vel4 * t
    t3 = (np.dot(n, pos[2]) + d) / (np.dot(n, vel[2]))
    t4 = (np.dot(n, pos[3]) + d) / (np.dot(n, vel[3]))
    print('collision times: ', t3, t4)
    pos3_x = pos[2][0] - vel[2][0] * t3
    pos3_y = pos[2][1] - vel[2][1] * t3
    pos3_z = pos[2][2] - vel[2][2] * t3
    print('pos3: ', pos3_x, pos3_y, pos3_z)
    #print('pos3: ', pos3_x + real_pos_0[0], pos3_y + real_pos_0[1], pos3_z + real_pos_0[2])

    pos4_x = pos[3][0] - vel[3][0] * t4
    pos4_y = pos[3][1] - vel[3][1] * t4
    pos4_z = pos[3][2] - vel[3][2] * t4
    print('pos4: ', pos4_x, pos4_y, pos4_z)
    vel_x = (pos4_x - pos3_x) / (t4 - t3)
    vel_y = (pos4_y - pos3_y) / (t4 - t3)
    vel_z = (pos4_z - pos3_z) / (t4 - t3)
    print('vel: ', vel_x, vel_y, vel_z)  # -3, 1, 2 after 0 substract
    pos_x = pos3_x - vel_x * t3
    pos_y = pos3_y - vel_y * t3
    pos_z = pos3_z - vel_z * t3
    print(pos_x, pos_y, pos_z)

    t = []
    for current_pos, current_vel in zip(pos, vel):
        t = np.dot(n, current_pos) / np.dot(n, current_vel)  # .append()
        # print(t, pos_x + vel_x * t, pos_y + vel_y * t, pos_z + vel_z * t, '*', current_pos[0] + current_vel[0] * t, current_pos[1] + current_vel[1] * t, current_pos[2] + current_vel[2] * t)

    return pos_x + pos_y + pos_z  # + sum(real_pos_0)  # 115 too low


if __name__ == '__main__':
    print(main())
