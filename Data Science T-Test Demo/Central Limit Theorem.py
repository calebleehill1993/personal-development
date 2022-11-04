import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

x = np.linspace(0, 20, 1000)
plt.plot(x, stats.gamma.pdf(x, 2, scale=2))
plt.show()
np.array(stats.gamma.pdf(x, a=3, scale=2) * x).mean()

y = stats.gamma.rvs(a=3, scale=2, size=10)
plt.hist(y)
plt.show()

sample_sizes = [[1, 2, 3, 4], [5, 10, 20, 30], [50, 100, 1000, 10000]]
plot, ax = plt.subplots(len(sample_sizes), len(sample_sizes[0]))
for i in range(len(sample_sizes)):
    for j in range(len(sample_sizes[1])):
        means = np.array([np.array(stats.uniform.rvs(loc=-100, scale=200, size=sample_sizes[i][j])).mean() for z in range(10000)])
        ax[i, j].hist(means, density=True, bins=20)
        ax[i, j].set_title(f'n =  {sample_sizes[i][j]}'.format())
        mean = means.mean()
        std_dev = np.array(stats.uniform.rvs(loc=-100, scale=200, size=sample_sizes[i][j])).std(ddof=1)
        sigma = 200/np.sqrt(12)
        std_err_norm = sigma / np.sqrt(sample_sizes[i][j])
        x = np.linspace(mean - 4 * std_err_norm, mean + 4 * std_err_norm, 1000)
        ax[i, j].plot(x, stats.norm.pdf(x, loc=mean, scale=std_err_norm), color='red')
plt.show()



