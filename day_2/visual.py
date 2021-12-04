from day_2.first import parse_instructions_from_input, Submarine, Direction
from day_2.second import SubmarineWithAim
from matplotlib import pyplot as plt
import matplotlib.animation as animation

part_1 = True
file_name = "part_1.mp4" if part_1 else "part_2.mp4"

instructions = parse_instructions_from_input("input.txt")
# replace Submarine instances with SubmarineWithAim to simulate part 2
if part_1:
    complete_sub = Submarine()
else:
    complete_sub = SubmarineWithAim()

xs = [0]
ys = [0]
for instruction in instructions:
    complete_sub.follow_instruction(instruction.direction, instruction.value)
    xs.append(complete_sub.horizontal)
    ys.append(-complete_sub.depth)

fig = plt.figure(figsize=(8, 6))
axis = plt.axes(
    xlim=(0, complete_sub.horizontal + 10), ylim=(-complete_sub.depth - 10, 0)
)
if part_1:
    axis.set_title("Submarine Movement (Part 1)")
else:
    axis.set_title("Submarine Movement (Part 2)")

plt.xlabel("Horizontal Distance")
plt.ylabel("Depth")
(line,) = axis.plot([], [], lw=3)

instructions = parse_instructions_from_input("input.txt")
if part_1:
    submarine = Submarine()
else:
    submarine = SubmarineWithAim()
xs, ys = [submarine.horizontal], [-submarine.depth]


# data which the line will
# contain (x, y)
def init():
    line.set_data(xs, ys)
    return (line,)


def animate(i):
    if len(instructions) > 0:
        instruction = instructions.pop(0)
        submarine.follow_instruction(instruction.direction, instruction.value)
        while instruction.direction != Direction.Forward and len(instructions) > 0:
            instruction = instructions.pop(0)
            submarine.follow_instruction(instruction.direction, instruction.value)
        xs.append(submarine.horizontal)
        ys.append(-submarine.depth)
        line.set_data(xs, ys)

    return (line,)


if __name__ == "__main__":
    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=len(instructions) + 10,
        interval=10,
        blit=True,
    )
    anim.save(file_name, writer="ffmpeg", fps=60)
