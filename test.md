graph TB
    Start(开始) --> Open[打开冰箱门]
    Open --> Put[把大象放进去]
    Put[把大象放进去] --> IsFit{"冰箱小不小？"}
    
    IsFit -->|不小| Close[把冰箱门关上]
    Close --> End(结束)
        
    IsFit -->|小| Change[换个大冰箱]
    Change --> Open
