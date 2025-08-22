// internal/reporter/reporter.go
package reporter

import (
	"fmt"
	"log"
	"os"
)

var (
	yellow = "\033[93m"
	green  = "\033[92m"
	red    = "\033[91m"
	gray   = "\033[90m"
	reset  = "\033[0m"
	colors = []string{"\033[95m", green, yellow, red}

	logFile *os.File
)

func init() {
	var err error
	logFile, err = os.OpenFile("fs_watcher.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("[ERROR] Failed to open log file:", err)
	}
	log.SetOutput(logFile)
}

// GetColor returns a color string based on index.
func GetColor(index int) string {
	return colors[index%len(colors)]
}

// PrintInfo prints a formatted informational message.
func PrintInfo(format string, a ...interface{}) {
	msg := fmt.Sprintf(format, a...)
	fmt.Printf("%s[INFO]%s %s%s\n", yellow, reset, msg, reset)
	log.Printf("[INFO] %s\n", msg)
}

// PrintError prints a formatted error message.
func PrintError(format string, a ...interface{}) {
	msg := fmt.Sprintf(format, a...)
	fmt.Printf("%s[ERROR]%s %s%s\n", red, reset, msg, reset)
	log.Printf("[ERROR] %s\n", msg)
}

// PrintIdle prints a formatted idle message for a given directory.
// func PrintIdle(dir string) {
// 	msg := fmt.Sprintf("%sNo activity in%s %s", Gray(), Reset(), dir)
// 	fmt.Printf("%s[IDLE]%s %s%s\n", gray, reset, msg, reset)
// 	log.Printf("[IDLE] %s\n", msg)
// }

// func PrintIdle(dir string) {
// 	msg := fmt.Sprintf("%sNo activity in %s%s", gray, dir, reset)
// 	fmt.Printf("%s[IDLE]%s %s%s", gray, reset, msg, reset)
// 	log.Printf("[IDLE] %s", msg)
// 	return
// 	}

func PrintIdle(dir string) {
	msg := fmt.Sprintf("No activity in %s", dir)
	// fmt.Printf("%s[IDLE] %s%s%s", gray, gray, msg, reset)
	fmt.Printf("%s[IDLE] %sNo activity in %s%s%s\n", gray, gray, dir, reset, reset)
	log.Printf("[IDLE] %s", msg)
}

// LogOnly writes to log file only, without terminal output.
func LogOnly(format string, a ...interface{}) {
	msg := fmt.Sprintf(format, a...)
	log.Printf("[LOG] %s\n", msg)
}

// Reset returns the ANSI reset color code.
func Reset() string {
	return reset
}

// / PrintRaw prints a raw preformatted message without any [INFO], [ERROR] prefix.
// Still logs to file.
func PrintRaw(msg string) {
	fmt.Println(msg)
	log.Println(msg)
}

func Yellow() string {
	return yellow
}

func Green() string {
	return green
}

func Gray() string {
	return gray
}

func Red() string {
	return red
}
