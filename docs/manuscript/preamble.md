# Native PDF preamble

This reviewed, hash-bound input is staged for docxology/template's combined PDF
renderer. Body sections cannot inject raw renderer markup. Package and theorem
declarations below keep the native template's content support explicit.

```latex
\usepackage{graphicx}
\usepackage{listings}
\lstset{basicstyle=\ttfamily\small,breaklines=true,columns=fullflexible}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{remark}[theorem]{Remark}
\newtheorem{example}[theorem]{Example}
```
