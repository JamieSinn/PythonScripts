package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/dutchcoders/goftp"
	"github.com/sinndevelopment/golib"
)

func main() {
	var err error
	var ftp *goftp.FTP
	if !handleArgs() {
		panic("Usage: ./logdl <host> <user> <password> <directory>")
	}
	args := os.Args[1:]
	host := args[0]
	user := args[1]
	pass := args[2]
	dir := golib.GetFinalArgs(args, 3)

	if ftp, err = goftp.Connect(host + ":21"); err != nil {
		panic(err)
	}
	defer ftp.Close()
	if err = ftp.Login(user, pass); err != nil {
		panic(err)
	}
	if err = ftp.Cwd(dir); err != nil {
		panic(err)
	}
	var curpath string
	if curpath, err = ftp.Pwd(); err != nil {
		panic(err)
	}

	downloadDirectory(curpath, ftp)
}

func downloadDirectory(directory string, ftp *goftp.FTP) {
	var files []string
	var err error
	if files, err = ftp.List(""); err != nil {
		panic(err)
	}
	directory = strings.Replace(directory, "\r\n", "", -1)

	for f := range files {
		filename := strings.Split(files[f], "; ")
		newPath := directory + "/" + filename[1]
		if !strings.Contains(filename[0], "type=dir;") {
			downloadFile(newPath, ftp)
		} else {
			ftp.Cwd(newPath)
			downloadDirectory(newPath, ftp)
		}
	}
}

func downloadFile(file string, ftp *goftp.FTP) {
	fmt.Println("Downloading: " + file)
}

func handleArgs() bool {
	args := os.Args[1:]
	return len(args) >= 4
}
