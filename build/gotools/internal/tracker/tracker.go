package tracker

import (
	"os"
	"path/filepath"
)

// DirStats holds basic information about a directory's contents.
type DirStats struct {
	FileCount int
	FileTypes map[string]int
}

// AnalyzeDir scans the directory recursively and collects statistics
// such as number of files and distribution of file types.
func AnalyzeDir(dirPath string) (*DirStats, error) {
	stats := &DirStats{
		FileCount: 0,
		FileTypes: make(map[string]int),
	}

	err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			stats.FileCount++

			// Delegate file type detection to shared function
			fileType := DetectFileType(path)
			stats.FileTypes[fileType]++
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	return stats, nil
}

// // internal/tracker/tracker.go
// package tracker

// import (
// 	"os"
// 	"path/filepath"
// )

// // DirStats holds basic information about a directory's contents.
// type DirStats struct {
// 	FileCount int
// 	FileTypes map[string]int
// }

// // AnalyzeDir scans the directory recursively and collects statistics
// // such as number of files and distribution of file types.

// func AnalyzeDir(dirPath string) (*DirStats, error) {
// 	stats := &DirStats{
// 		FileCount: 0,
// 		FileTypes: make(map[string]int),
// 	}

// 	err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
// 		if err != nil {
// 			return err
// 		}
// 		if !info.IsDir() {
// 			stats.FileCount++
// 			ext := filepath.Ext(path)
// 			if ext == "" {
// 				ext = "noext"
// 			}
// 			stats.FileTypes[ext]++
// 		}
// 		return nil
// 	})

// 	if err != nil {
// 		return nil, err
// 	}

// 	return stats, nil
// }
