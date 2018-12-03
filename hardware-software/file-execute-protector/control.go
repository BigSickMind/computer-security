package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"runtime"
	"strconv"
	"strings"
)

const params = "blk|________________________________________________________________|end"

func get_drive_serial(disk string)(string) {
	cmd := exec.Command("powershell", "/C", "Get-Partition | % {New-Object PSObject -Property @{'DriveLetter'=$_.DriveLetter; 'SerialNumber'=(Get-Disk $_.DiskNumber).SerialNumber}}")
	cmdOutput := &bytes.Buffer{}; cmd.Stdout = cmdOutput
	err := cmd.Run(); if err != nil {log.Fatal(err)}
	get_serial := string(cmdOutput.Bytes())
	splitted := strings.Split(get_serial, "\n")
	for i := 3; i < len(splitted) - 3; i++ {
		str := splitted[i][10:]; idx := strings.Index(str, " ")
		dsk := str[:idx]; serial := ""
		for j := idx; j < len(str); j++ {if str[j] != ' ' {serial += string(str[j])}}
		if serial[len(serial) - 1] == '\r' || serial[len(serial) - 1] == '\n' {serial = serial[:len(serial) - 1]}
		if dsk == disk {return serial}
	}
	return ""
}

func get_hash(file string)(string) {
	h := sha256.New()
	io.WriteString(h, file)
	hash := hex.EncodeToString(h.Sum(nil))
	return hash
}

func get_info(filepath string, file []uint8)([]string) {
	fi, _ := os.Stat(filepath); idx := strings.LastIndex(fi.Name(), ".")
	filename := fi.Name()[:idx]; size := strconv.Itoa(len(file))
	hash := get_hash(string(file))
	disk := filepath[:strings.Index(filepath, ":")]; serial := get_drive_serial(disk)
	info := []string{filename, size, hash, serial}
	return info
}

func main() {
	_, filepath, _, _ := runtime.Caller(0)
	file, _ := ioutil.ReadFile(filepath)
	file_str := string(file)
	start := strings.Index(file_str, "blk|"); end := strings.Index(file_str, "|end")
	if file_str[start + 4] == '_' {
		info := get_info(filepath, file); info_string := strings.Join(info, "|"); hash_info := get_hash(info_string)
		data :=[]byte(file_str[:start + 4] + hash_info + file_str[end:])
		err := ioutil.WriteFile(filepath, data, 0644); if err != nil {log.Fatal(err)}
	} else {
		hash_parameters := file_str[start + 4:end]
		file_byte := []uint8(file_str[:start + 4] + "________________________________________________________________" + file_str[end:])
		info := get_info(filepath, file_byte); info_string := strings.Join(info, "|"); hash_info := get_hash(info_string)
		if hash_info != hash_parameters {fmt.Println("Error! Incorrect file parameters. Verification failed")} else {
			fmt.Println("Verification passed successfully")}
	}
}