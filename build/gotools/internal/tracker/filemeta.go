// internal/tracker/filemeta.go
package tracker

import (
	"os"
	"path/filepath"
	"strings"
)

// FileMeta holds basic file information.
type FileMeta struct {
	Size    int64
	ModTime int64
	Type    string
}

// AnalyzeFile returns basic metadata about the file.
func AnalyzeFile(path string) (*FileMeta, error) {
	info, err := os.Stat(path)
	if err != nil {
		return nil, err
	}

	fileType := DetectFileType(path)
	return &FileMeta{
		Size:    info.Size(),
		ModTime: info.ModTime().Unix(),
		Type:    fileType,
	}, nil
}

func DetectFileType(path string) string {
	base := filepath.Base(path)
	if !strings.Contains(base, ".") || strings.HasPrefix(base, ".") && !strings.Contains(base[1:], ".") {
		return "unknown"
	}

	ext := strings.ToLower(filepath.Ext(base))
	if ext == "" {
		return "unknown"
	}
	return ext[1:] // remove dot
}

// #################################################################
// DetectFileType returns a basic string representing the file type.
// func DetectFileType(path string) string {
// 	ext := strings.ToLower(filepath.Ext(path))
// 	if ext == "" {
// 		return "unknown"
// 	}
// 	return ext[1:] // remove the dot
// }

// func DetectFileType(path string) string {
// 	ext := strings.ToLower(filepath.Ext(path))
// 	if ext == "" || len(ext) == 1 { // catches names like ".hidden"
// 		return "unknown"
// 	}
// 	return ext[1:] // remove the dot
// }
// #################################################################