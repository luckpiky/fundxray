
  # Fund X-Ray设计

  ## 1 基金数据收集
  程序名：catch_data
  描述：从新浪基金数据网站获取数据，通过程序参数指定基金编码，获取的页面数，以及存储的csv文件。  
  参数：  
  -p n 指定读取的页数  
  -a 指定读取所有页的内容  
  -d 指定csv的目录  
  -c 处理的基金的编码  

```
@startuml
start
: 解析参数;
: 获取数据;
: 写入文件;
stop
@enduml
```

### 1.1 写入数据
从文件中先读取所有数据，然后将页面中的数据与该数据进行插入排序，然后再写入到文件中。插入时，需要排除已经存在的数据。

```
@startuml
start
: 读取文件中的数据;
: 插入页面中的数据排序;
: 写入文件;
stop
@enduml
```
