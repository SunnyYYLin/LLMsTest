本题将介绍“加窗＂的概念，它尤论在线性时不变系统的设计，还是在信号的频谱分析中都非常重要。  
“加窗”就是把信号 x[n] 乘以一个有限长的窗口信号 w[n] 的一种运算，也就是  
$p[n] = x[n]w[n]$   
注意， p[n] 也是有限长的。
在频谱分析中，加街的重要性来自于：在大址应用场合，人们总是希望计算被测信号的傅里叶变换。  
由千在实际中只能在有限时间区间（即时窗）上测得信号 x[n] ，因而对频谱分析来说，实际可利用的信号是  
$$
p[n]=\left\{
\begin{aligned}
x[n] & ,-M \leqslant n \leqslant M \\
0 & ,其他\\
\end{aligned}
\right.
$$
其中$－M\leqslant n \leqslant M$就是时窗。于是  
$p[n]=x[n]w[n]$  
这里 w[n] 是矩形窗，即  
$$
w[n]=\left\{
\begin{aligned}
1 & ,-M \leqslant n \leqslant M \\
0 & ,其他 & (P5.55-1)\\
\end{aligned}
\right.
$$
“加窗”在线性时不变系统设计中也起着重要的作用。具体而言，由于种种原因 ，需要设计一个具有有限长脉冲响应的系统，以便达到某种要求的信
号处理目的；也就是说，往往从所需的频率响应$H(e^{j \omega})$开始，它的逆变换 h[n] 是一个无限长（或至少是非常长）的单位脉冲响应，而要求构成一个有限长单位脉冲响应 g[n] ，使它的傅里叶变换$G(e^{j \omega})$充分地逼近$H(e^{j \omega})$。选择 g[n] 的一般方法是找一个窗函数 w[n] ，使 h[n]w[n] 的傅里叶变换满足所需
$G(e^{j \omega})$的指标要求。  
很明显，将一个信号加窗对所得到的频谱是会有影响的，本题将说明这种影响。  
为了对加窗的效果加深理解，现用式(PS. 55-1) 所给的矩形窗对信号  
$x[n]=\sum_{k=-\infty}^{\infty}\delta[n-k]$  
进行加窗。  
(i) $X(e^{j \omega})$ 是什么？  
(ii) M=1 时，概略画出 p[n] =x[n]w[n] 的变换。  
(iii) M=10 时，重做 (ii)  

In this problem we introduce the concept of windowing, which is of great importance 
both in the design of LTI systems and in the spectral analysis of signals. Windowing 
is the operation of taking a signal x[ n] and multiplying it by a finite-duration window 
signal w[n]. That is,    
$p[n] = x[n]w[n]$   
Note that p[n] is also of finite duration.   
The importance of windowing in spectral analysis stems from the fact that in numerous applications one wishes to compute the Fourier transform of a signal that has been measured. Since in practice we can measure a signal x[n] only over a finite time interval (the time window), the actual signal available for spectral analysis is  
$$
p[n]=\left\{
\begin{aligned}
x[n] & ,-M \leqslant n \leqslant M \\
0 & ,otherwise\\
\end{aligned}
\right.
$$
where $－M\leqslant n \leqslant M$ is the time window. Thus,  
$p[n]=x[n]w[n]$    
where w[n] is the rectangular window; that is,  
$$
w[n]=\left\{
\begin{aligned}
1 & ,-M \leqslant n \leqslant M \\
0 & ,otherwise & (P5.55-1)\\
\end{aligned}
\right.
$$
Windowing also plays a role in LTI system design. Specifically, for a variety of reasons, it is often advantageous to design a system that has an impulse response of finite duration to achieve some desired signal-processing objective. That is, we often begin with a desired frequency response $H(e^{j \omega})$ whose inverse transform h[n] is an impulse response of infinite (or at least excessively long) duration. What is required then is the construction of an impulse response g[ n] of finite duration whose transform $G(e^{j \omega})$ adequately approximates $H(e^{j \omega})$ . One general approach to choosing g[n] is to find a window function w[n] such that the transform of h[n]w[n] meets the desired specifications for $G(e^{j \omega})$.   
Clearly, the windowing of a signal has an effect on the resulting spectrum. In this problem, we illustrate that effect.  

To gain some understanding of the effect of windowing, consider windowing the signal  
$x[n]=\sum_{k=-\infty}^{\infty}\delta[n-k]$  
using the rectangular window signal given in eq. (P5.55-1).  
(i) What is $X(e^{j \omega})$?   
(ii) Sketch the transform of p[n] = x[n]w[n] when M = 1.   
(iii) Do the same for M = 10.  
