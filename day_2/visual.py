from day_2.first import parse_instructions_from_input, Submarine
from day_2.second import SubmarineWithAim
from matplotlib import pyplot as plt
import matplotlib.animation as animation


instructions = parse_instructions_from_input("input.txt")
# replace Submarine instances with SubmarineWithAim to simulate part 2
complete_sub = Submarine()
xs = [0]
ys = [0]
for instruction in instructions:
    complete_sub.follow_instruction(instruction.direction, instruction.value)
    xs.append(complete_sub.horizontal)
    ys.append(-complete_sub.depth)

fig = plt.figure()
axis = plt.axes(xlim=(0, complete_sub.horizontal + 10),
                ylim=(-complete_sub.depth - 10, 0))
line, = axis.plot([], [], lw=3)

submarine = Submarine()
xs, ys = [submarine.horizontal], [-submarine.depth]


# data which the line will
# contain (x, y)
def init():
    submarine = Submarine()
    xs, ys = [submarine.horizontal], [-submarine.depth]
    line.set_data(xs, ys)
    return line,


def animate(i):
    if i < len(instructions):
        submarine.follow_instruction(instructions[i].direction, instructions[i].value)
        xs.append(submarine.horizontal)
        ys.append(-submarine.depth)
        line.set_data(xs, ys)

    return line,


if __name__ == "__main__":
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(instructions)+10, interval=10, blit=True)
    anim.save('part_1.mp4', writer='ffmpeg', fps=60)
