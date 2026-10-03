![图 12.10：山地车任务上 Sarsa(λ) 与 n 步 Sarsa 的早期表现](assets/fig-12-10.png)

**图 12.10**　山地车任务上，采用替换迹的 Sarsa(\(\lambda\)) 与 \(n\) 步 Sarsa（复制自图 10.4）的早期表现，横向比较步长 \(\alpha\) 的影响。

图内文字译注：左图标题 Sarsa(\(\lambda\)) with replacing traces＝“采用替换迹的 Sarsa(\(\lambda\))”；右图标题 n-step Sarsa＝“\(n\) 步 Sarsa”；纵轴 Mountain Car Steps per episode averaged over first 50 episodes and 100 runs＝“山地车：前 50 个回合、100 次运行平均的每回合步数”；两图横轴 \(\alpha\times\) number of tilings (8)＝“\(\alpha\times\) 铺砌数（8）”。左图曲线标有 \(\lambda=0,0.68,0.84,0.92,0.96,0.98,0.99\)（部分值在曲线两端重复标示）；右图曲线标有 \(n=1,2,4,8,16\)（部分值重复标示）。

![图 12.11：山地车任务上 Sarsa(λ) 算法的总体比较](assets/fig-12-11.png)

**图 12.11**　山地车任务中 Sarsa(\(\lambda\)) 算法的总体比较。真在线 Sarsa(\(\lambda\)) 的表现优于使用累积迹或替换迹的常规 Sarsa(\(\lambda\))。图中还包括一种采用替换迹的 Sarsa(\(\lambda\)) 版本：在每个时间步，将当前状态中未选行动对应的迹置零。

图内文字译注：纵轴 Mountain Car Reward per episode averaged over first 20 episodes and 100 runs＝“山地车：前 20 个回合、100 次运行平均的每回合奖励”；横轴 \(\alpha\times\) number of tilings (8)＝“\(\alpha\times\) 铺砌数（8）”；四条曲线分别为 True online Sarsa(\(\lambda\))＝“真在线 Sarsa(\(\lambda\))”、Sarsa(\(\lambda\)) with replacing traces＝“采用替换迹的 Sarsa(\(\lambda\))”、Sarsa(\(\lambda\)) with replacing traces and clearing the traces of other actions＝“采用替换迹并清除其他行动的迹的 Sarsa(\(\lambda\))”、Sarsa(\(\lambda\)) with accumulating traces＝“采用累积迹的 Sarsa(\(\lambda\))”。
