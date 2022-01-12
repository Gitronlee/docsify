# Golang开发小工具时用到的包

昨天开发了一个小工具，不过这次用的是Golang写的，在此记录下用到的轮子。

工具的逻辑包括从html提取必要信息，将html转为pdf，调用外部exe工具统计信息，根据以上各信息计算，并输出到doc，还有必要的高亮显示的打印信息。

## 多任务

若要起n个协程的任务，设置一个带缓冲的chan，在每个协程中对其填，用n次循环取之，取完循环不再阻塞。

```go
func Conv2PDF(reportsNum int) {
//开reportsNum  个协程
	done := make(chan string, reportsNum)
	i := 0
	for _, k := range Config.ModuleList {
		for _, v := range k.ReportLst {
			i++
			go func(vv string) {
				pdfOpt := NewPdf(Config.Wkhtmltopdf, path.Join(WorkDir, "report_html"))
				pdfOpt.OutFile(path.Join(WorkDir, "report_html", vv+".html"), path.Join(WorkDir, "result", "pdf", vv+".pdf"))
				done <- vv
			}(v)
		}
	}
	//等待N个后台线程完成
	for i := 0; i < cap(done); i++ {
		fmt.Printf("%s\t转为PDF结束...\n", <-done)
	}
}
```

## "os/signal"

限制程序结束后，以CTRL-C退出。Notify函数让signal包将输入信号转发到c。如果没有列出要传递的信号，会将所有输入信号传递到c；否则只传递列出的输入信号。可通过对c的取阻塞之。

```go
c := make(chan os.Signal, 1)
signal.Notify(c, os.Interrupt, os.Kill)
s := <-c
fmt.Println("Got signal:", s)
```

## "github.com/spf13/viper"

viper的配置需要注意结构体成员的对外可见性（首字母大写）。Unmarshal到结构体的方式对一些map形式可以保证其顺序为预期。

```go
workDir, _ := os.Getwd()
viper.SetConfigName("application")
viper.SetConfigType("yml")
viper.AddConfigPath(workDir + "/config")
viper.SetDefault("workDir", workDir)
//根据用户选择 可设置不同的配置
viper.SetDefault("xxx", "asasasdsad")
err := viper.ReadInConfig()
if err != nil {
    panic(err)
}
...
//读取多个配置文件
if a1 == 1 {
viper.SetConfigName("ATP-UT")
viper.AddConfigPath(WorkDir + "/config")
viper.MergeInConfig()
if err != nil {
log.Fatalf("读取%d号配置出错:%v", a1, err)
}
break
}
...
err = viper.Unmarshal(&Config)
...
//得到 cloc 下的配置（map[string] interface{} 类型）,并对此map遍历
needMap := viper.GetStringMap(viper.GetString("xxx"))
UTITlist := viper.GetStringSlice(viper.GetString("xxx") + "." + k + "." + viper.GetString("yyy"))
```

## "path/filepath"

扩展名相关和路径拼接。

```go
ext := filepath.Ext(outPath)//获取扩展名
path.Join(WorkDir, "report_html", v+".html")//路径拼接
```

## "os/exec"

cmd里执行命令，打印时可能有乱码。

```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()
//fmt.Println(thisHtmlToPdf.prams)
cmd := exec.CommandContext(ctx, thisHtmlToPdf.Commond, thisHtmlToPdf.prams...)
stdout, err := cmd.StderrPipe()
if err != nil {
    return nil, err
}
defer stdout.Close()
//运行命令
err = cmd.Start()
if err != nil {
    return nil, err
}
bytes, err := ioutil.ReadAll(stdout)
if err != nil {
    return nil, err
}
//等待完成
cmd.Wait()
return bytes, err
```

```go
cmdOutput, err := exec.Command(viper.GetString("clocpath"), paths).Output()
if err != nil {
    log.Fatal(err)
}
scanner := bufio.NewScanner(bytes.NewReader(cmdOutput))
//读取输出结果，并对某行特殊处理
for scanner.Scan() {
    line := scanner.Text() // or
    //line := scanner.Bytes()
    //do_your_function(line)
    if len(line) > 1 && line[0] == 'C' && line[1] == ' ' {
        //Fields方法移除连续的空白符号
        //strings.TrimSpace(res)删除首尾空白
        res = (strings.Fields(line))[4]
    }

}
for scanner.Scan() {
//字符转换，解决cmd打印乱码问题
    cmdRe := ConvertByte2String(scanner.Bytes(), "GB18030")
    if index := strings.Index(cmdRe, "vcxproj ->"); index != -1 {
        c.Println("已完成:\t", cmdRe)
    } else if index := strings.Index(cmdRe, ": error"); index != -1 {
        r.Println("出错了:\t", cmdRe)
        return -1
    }

}
//fmt.Printf("%s", cmdOutput)
```

## "io"

```go
//文件拷贝
func copyFile2(srcFile, destFile string) (int64, error) {
	file1, err := os.Open(srcFile)
	if err != nil {
		return 0, err
	}
	file2, err := os.OpenFile(destFile, os.O_WRONLY|os.O_CREATE, os.ModePerm)
	if err != nil {
		return 0, err
	}
	defer file1.Close()
	defer file2.Close()

	return io.Copy(file2, file1)
}
```

## "runtime"

相比于获取工作路径，有时获取当前文件的路径更有用。

```go
//获取当前文件路径
func getCurrentPath() string {
	_, filename, _, ok := runtime.Caller(1)
	var cwdPath string
	if ok {
		cwdPath = path.Join(path.Dir(filename), "") // the the main function file directory
	} else {
		cwdPath = "./"
	}
	return cwdPath
}
```

## "golang.org/x/text/encoding/simplifiedchinese"

```go
//将byte转为string
func ConvertByte2String(byte []byte, charset Charset) string {
	var str string
	switch charset {
	case GB18030:
		var decodeBytes, _ = simplifiedchinese.GB18030.NewDecoder().Bytes(byte)
		str = string(decodeBytes)
	case UTF8:
		fallthrough
	default:
		str = string(byte)
	}
	return str
}
```

## "strconv"

```go
i, err := strconv.ParseFloat(res, 64)//字符串转float64
```

## "baliance.com/gooxml/document"

对文档里的表格操作，这个包的各种属性优点乱：）。

```go
func WriteToDoc() {
	doc, _ := document.Open(path.Join(WorkDir, "static", Config.TemplateDoc))
	table := doc.Tables()[0]//获得第一个表
	row := table.AddRow()//增加一行
	AddaCell(MapItemsToNum[Item], row, n)
	doc.SaveToFile(path.Join(WorkDir, "result", "doc", Config.TemplateDoc))
}
func AddaCell(val string, row document.Row, cols int) {
	cell := row.AddCell()
	cell.Properties().SetColumnSpan(cols)//设置单元格横向合并
	cellAddPara := cell.AddParagraph()
	cellAddPara.Properties().SetAlignment(wml.ST_JcCenter)//居中
	cellAddParaRun := cellAddPara.AddRun()
	cellAddParaRun.AddText(val)
	cellAddParaRun.Properties().SetSize(10.5)//设置字号
}
```

## "github.com/PuerkitoBio/goquery"

selector选择器使用

```go
f, _ := ioutil.ReadFile(url)
dom, err := goquery.NewDocumentFromReader(strings.NewReader(string(f)))
if err != nil {
    log.Fatalln(err)
}

dom.Find("body > table > tbody > tr:nth-child(2) > td > table:nth-child(6) > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(4) > td:nth-child(7)").Each(func(i int, selection *goquery.Selection) {
    res = selection.Text()
})
//strings.TrimSpace(res) 去除首尾空白
testCases, err := strconv.ParseFloat(strings.TrimSpace(res), 64)
```

## "log"

可以设置flag实现时间，文件名，行号等的log

```go
//d.go:23 日期及时间
log.SetFlags(log.Lshortfile | log.LstdFlags)
f1, _ := os.OpenFile("./log.log", os.O_APPEND|os.O_WRONLY, 0666) //打开文件,第二个参数是写入方式和权限
log.SetOutput(f1)
```

## "github.com/fatih/color"

```go
c := color.New(color.FgCyan)//华丽显示
c.Printf(xxxx)
```
