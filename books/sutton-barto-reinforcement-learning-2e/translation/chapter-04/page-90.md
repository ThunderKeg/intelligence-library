**4.5** 异步 DP 算法由 Bertsekas（1982，1983）提出，他也把它们称为**分布式 DP 算法**。提出异步 DP 最初是为了在多处理器系统上实现 DP；这种系统中的处理器之间存在通信延迟，而且没有全局同步时钟。Bertsekas 和 Tsitsiklis（1989）详细讨论了这些算法。Jacobi 式和 Gauss–Seidel 式 DP 算法都是异步版本的特例。Williams 和 Baird（1990）提出的 DP 算法，比本书讨论的算法具有更细的异步粒度：更新操作本身被拆成可以异步执行的多个步骤。

**4.7** 本节在 Michael Littman 的帮助下写成，以 Littman、Dean 和 Kaelbling（1995）为基础。“维度灾难”这一说法来自 Bellman（1957a）。

强化学习的线性规划方法方面的奠基工作由 Daniela de Farias 完成（de Farias，2002；de Farias 和 Van Roy，2003）。
