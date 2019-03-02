package main

import (
	"container/list"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"
	"encoding/csv"
	"os"
	"flag"
	"time"
	"sort"
)


/* 定义sina基金的json格式 */
type SA struct {
	name string
	age  int
}

type JiJinCode struct {
	Code int
}

type JiJinStatus struct {
	Status JiJinCode
}

type JiJinData struct {
	Fbrq string
	Jjjz string
	Ljjz string
}

type JiJinDataArray struct {
	Data      []JiJinData
	Total_num string
}

type JiJinDataResult struct {
	Status JiJinCode
	Data   JiJinDataArray
}

type JiJinResult struct {
	Result JiJinDataResult
}


func GetFundDataFromSina(fundCode string, fundPage int, fundDataList *list.List) int {

	var fundUrl = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=CODE&page=PAGE"
	fundPageStr := strconv.Itoa(fundPage)

	fundUrl = strings.Replace(fundUrl, "CODE", fundCode, -1)
	fundUrl = strings.Replace(fundUrl, "PAGE", fundPageStr, -1)

	log.Println("读取URL:" + fundUrl)

	httpClient := &http.Client{Timeout:5*time.Second,}
	req, err := http.NewRequest("POST", fundUrl, strings.NewReader(""))
	//req.Header.Add("Con")

	resp, err := httpClient.Do(req)
	if err != nil {
		log.Println(err)
		return  -1
	}

	//def resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Println(err)
		return -2
	}

	json_str := string(body)
	//fmt.Println(json_str)

	var data JiJinResult
	if err := json.Unmarshal([]byte(json_str), &data); err == nil {

		count := len(data.Result.Data.Data)
		for i := 0; i < count; i++ {
			data1 := data.Result.Data.Data[i]
			//fmt.Println(data1.Fbrq, data1.Jjjz, data1.Ljjz)
			fundDataList.PushBack(data1)
		}

		return count
	} else {
		fmt.Println(err)
		return -3
	}
}

//对[][]string排序
type FundDataSlice [][]string

func (a FundDataSlice) Len() int {    // 重写 Len() 方法
    return len(a)
}

func (a FundDataSlice) Swap(i, j int){     // 重写 Swap() 方法
    a[i], a[j] = a[j], a[i]
}

func (a FundDataSlice) Less(i, j int) bool {    // 重写 Less() 方法， 从大到小排序

	tm1, _ := time.Parse("2006-01-02 15:04:05", a[i][0])
	tm2, _ := time.Parse("2006-01-02 15:04:05", a[j][0])

    return tm2.After(tm1)
}

func WriteFundDataToCsv(fileName string, fundDataList *list.List) {
	var oldData [][]string

	//读取老数据
	readContent,err := ioutil.ReadFile(fileName)
	if err == nil {
		csvReadFp := csv.NewReader(strings.NewReader(string(readContent)))
		oldData,_ = csvReadFp.ReadAll()
		log.Println("读取到老数据条目数：",len(oldData))
	}

	f, err := os.Create(fileName)//创建文件
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := csv.NewWriter(f)//创建一个新的写入文件流

	//检查是否有已经存在，如果未存在则插入
	for item:= fundDataList.Back(); item != nil; item= item.Prev() {
		isExist := false
		
		data1 := item.Value.(JiJinData)

		for i := 0; i < len(oldData);i++{
			
			if oldData[i][0] == data1.Fbrq {
				isExist = true
				break
			}
		}

		if false == isExist{
			data2 := []string{data1.Fbrq, data1.Jjjz, data1.Ljjz}
			oldData = append(oldData, data2)
		}
	}

	sort.Sort(FundDataSlice(oldData)) 

	for i := 0; i < len(oldData);i++{
		data := [][]string{oldData[i]}
		w.WriteAll(data)//写入数据
	}

	log.Println("读取数据条目数：", fundDataList.Len())
	log.Println("写入数据条目数：",len(oldData))

	w.Flush()
}

var fundCode = flag.String("c", "", "基金编码")
var pageCount = flag.Int("p", 1,  "读取的页数")
var isReadAllPage = flag.Bool("a", false,  "读取所有的页数")
var saveDir = flag.String("d", "./",  "csv文件输出目录")

func main() {

	flag.Parse()

	log.Println("基金编号：" + *fundCode)
	log.Println("读取所有页：" + strconv.FormatBool(*isReadAllPage))

	if *isReadAllPage != false {
		*pageCount = 999999
	}

	log.Println("读取页数：" + strconv.Itoa(*pageCount))

	data := list.New()

	for i := 1; i <= *pageCount; i++ {
		ret := GetFundDataFromSina(*fundCode, i, data)
		if  0 == ret {
			break
		}
	}

	if data.Len() == 0 {
		log.Println("没有获取到数据")
		return
	}

	WriteFundDataToCsv(*saveDir+*fundCode+".csv", data)
}
