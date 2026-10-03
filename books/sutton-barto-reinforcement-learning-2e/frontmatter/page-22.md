# 记号表（续）

| 记号 | 含义 |
| --- | --- |
| 𝐀 | d × d 矩阵，𝐀 ≐ 𝔼[𝐱ₜ(𝐱ₜ − γ𝐱ₜ₊₁)ᵀ] |
| 𝐛 | d 维向量，𝐛 ≐ 𝔼[Rₜ₊₁𝐱ₜ] |
| \(\mathbf w_{\mathrm{TD}}\) | TD 不动点，\(\mathbf w_{\mathrm{TD}}\) ≐ 𝐀⁻¹𝐛（d 维向量；第 9.4 节） |
| 𝐈 | 单位矩阵 |
| 𝐏 | 策略 π 下，表示状态转移概率的 \|𝒮\| × \|𝒮\| 矩阵 |
| 𝐃 | 对角线为 𝛍 的 \|𝒮\| × \|𝒮\| 对角矩阵 |
| 𝐗 | 以各个 𝐱(s) 为行的 \|𝒮\| × d 矩阵 |

| 记号 | 含义 |
| --- | --- |
| \(\bar\delta_{\mathbf w}(s)\) | 状态 s 处 \(v_{\mathbf w}\) 的贝尔曼误差（期望 TD 误差；第 11.4 节） |
| \(\bar{\boldsymbol\delta}_{\mathbf w}\)，BE | 贝尔曼误差向量，其各分量为 \(\bar\delta_{\mathbf w}(s)\) |
| \(\overline{\mathrm{VE}}(\mathbf w)\) | 均方价值误差，\(\overline{\mathrm{VE}}(\mathbf w)\) ≐ \(\lVert v_{\mathbf w}-v_\pi\rVert_\mu^2\)（第 9.2 节） |
| \(\overline{\mathrm{BE}}(\mathbf w)\) | 均方贝尔曼误差，\(\overline{\mathrm{BE}}(\mathbf w)\) ≐ \(\lVert\bar{\boldsymbol\delta}_{\mathbf w}\rVert_\mu^2\) |
| \(\overline{\mathrm{PBE}}(\mathbf w)\) | 均方投影贝尔曼误差，\(\overline{\mathrm{PBE}}(\mathbf w)\) ≐ \(\lVert\Pi\bar{\boldsymbol\delta}_{\mathbf w}\rVert_\mu^2\) |
| \(\overline{\mathrm{TDE}}(\mathbf w)\) | 均方时序差分误差，\(\overline{\mathrm{TDE}}(\mathbf w)\) ≐ \(\mathbb E_b[\rho_t\delta_t^2]\)（第 11.5 节） |
| \(\overline{\mathrm{RE}}(\mathbf w)\) | 均方回报误差（第 11.6 节） |
