# Mermaid

## Flow Chart

```mermaid
%% 声明图的种类和方向
%% 流程图的方向：TD(top-down), BT(bottom-top), RL(right-left), LR(left-right)
graph LR
    %% 声明节点，id["text"]
    A[rectangle]
    B(rounded rectangle)
    C((round))

    %% 连线
    %% 文档中还说能用A --- B & C的方式连同级节点，但是这个版本的typora渲染不出来
    A --text--> B --- C
    A ==> C
    
    %% 声明的同时连线
    C -.->|text| D>flag]
    C === E{"prism"}  %% 当标签中有特殊字符，如括号时，用双引号
    

    %% 子图
    subgraph one
        F[/parallelogram/] --> G[\parallelogram alt\]
    end
```

## Sequence Diagram

```mermaid
sequenceDiagram
    %% 声明成员（也可以不声明，不声明则不能起别名或者定义重名成员）
    participant A as Alice
    participant B as Bob
    
    %% 发送信息
    A -> B: solid line without arrow
    A--> B:	Dotted line without arrow
    A ->> B: Solid line with arrow
    A -->> B: Dotted line with arrow
    A -x B: Solid line with a cross at the end (async)
    A --x B: Dotted line with a cross at the end (async)
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Still
    Still --> [*]

    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```

```mermaid
stateDiagram-v2
    %% 起止状态
    [*] --> s1
    s1 --> [*]

    %% 先声明后连接。这样声明的节点可以包含空格等特殊字符，且长得不一样
    s2: state with description

    %% 连接线上的字
    [*] --> s2: transition
    
    %% 补充说明。可以是right of 或者 left of
    note right of s2
        You can write notes
    end note

    %% 嵌套状态
    state First{
        [*] --> second
        
        %% 虚线框分隔
        --
        
        [*]
    }
```



# flow

```flow
# 定义节点
st=>start: Start
op=>operation: Operation
cond=>condition: Condition
sub=>subroutine: Subroutine
io=>inputoutput: I/O
e=>end

# 连接节点
st->op->cond
cond(yes)->sub->io->e
cond(no)->e
```

