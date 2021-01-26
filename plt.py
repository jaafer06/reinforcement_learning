from reinforcement_learning import *
from matplotlib import pyplot as plt

sarsa: Sarsa = Sarsa.load("sarsa.p")


logs = sarsa.loss_length_wonlength
loss = list(map(lambda data: data[0], logs))

length_won = list(map(lambda data: data[2], logs))


plt.plot(loss)
plt.show()