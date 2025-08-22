package tracker

import (
	"os"
	"path/filepath"
	"testing"
)

func TestDetectFileType(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"file.txt", "txt"},
		{"archive.tar.gz", "gz"},
		{"no_extension", "unknown"},
		{".hiddenfile", "unknown"},
	}

	for _, tt := range tests {
		got := DetectFileType(tt.input)
		if got != tt.expected {
			t.Errorf("DetectFileType(%q) = %q; want %q", tt.input, got, tt.expected)
		}
	}
}

func TestAnalyzeFile(t *testing.T) {
	fileName := "test_file.txt"
	content := []byte("Hello World")
	err := os.WriteFile(fileName, content, 0644)
	if err != nil {
		t.Fatalf("Failed to create test file: %v", err)
	}
	defer os.Remove(fileName)

	meta, err := AnalyzeFile(fileName)
	if err != nil {
		t.Fatalf("AnalyzeFile returned error: %v", err)
	}

	if meta.Size != int64(len(content)) {
		t.Errorf("Expected size %d, got %d", len(content), meta.Size)
	}
	if meta.Type != "txt" {
		t.Errorf("Expected type \"txt\", got %q", meta.Type)
	}
	if meta.ModTime == 0 {
		t.Error("Expected non-zero ModTime")
	}
}

func TestAnalyzeDir(t *testing.T) {
	dirName := "test_dir"
	os.Mkdir(dirName, 0755)
	defer os.RemoveAll(dirName)

	file1 := filepath.Join(dirName, "file1.txt")
	file2 := filepath.Join(dirName, "file2.log")
	file3 := filepath.Join(dirName, "file3")

	os.WriteFile(file1, []byte("one"), 0644)
	os.WriteFile(file2, []byte("two"), 0644)
	os.WriteFile(file3, []byte("noext"), 0644)

	stats, err := AnalyzeDir(dirName)
	if err != nil {
		t.Fatalf("AnalyzeDir failed: %v", err)
	}

	if stats.FileCount != 3 {
		t.Errorf("Expected 3 files, got %d", stats.FileCount)
	}
	if stats.FileTypes["txt"] != 1 {
		t.Errorf("Expected 1 txt file, got %d", stats.FileTypes["txt"])
	}
	if stats.FileTypes["log"] != 1 {
		t.Errorf("Expected 1 log file, got %d", stats.FileTypes["log"])
	}
	if stats.FileTypes["unknown"] != 1 {
		t.Errorf("Expected 1 file with unknown extension, got %d", stats.FileTypes["unknown"])
	}
}

func TestAnalyzeFileNonExistent(t *testing.T) {
	_, err := AnalyzeFile("nonexistent_file.txt")
	if err == nil {
		t.Error("Expected error for nonexistent file, got nil")
	}
}

func TestAnalyzeDirInvalidPath(t *testing.T) {
	_, err := AnalyzeDir("/this/path/does/not/exist")
	if err == nil {
		t.Error("Expected error for invalid directory path, got nil")
	}
}

func TestAnalyzeDirHiddenFile(t *testing.T) {
	dirName := "test_dir_hidden"
	os.Mkdir(dirName, 0755)
	defer os.RemoveAll(dirName)

	hiddenFile := filepath.Join(dirName, ".hiddenfile")
	os.WriteFile(hiddenFile, []byte("hidden"), 0644)

	stats, err := AnalyzeDir(dirName)
	if err != nil {
		t.Fatalf("AnalyzeDir failed: %v", err)
	}

	found := false
	for ext := range stats.FileTypes {
		if ext == "unknown" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Expected at least one file with unknown extension, found none. Got: %+v", stats.FileTypes)
	}
}

func TestAnalyzeDirPermissionDenied(t *testing.T) {
	dirName := "test_dir_perm"
	os.Mkdir(dirName, 0000)
	defer func() {
		os.Chmod(dirName, 0755)
		os.RemoveAll(dirName)
	}()

	_, err := AnalyzeDir(dirName)
	if err == nil {
		t.Error("Expected permission error, got nil")
	}
}


// #################################################################

// package tracker

// import (
// 	"os"
// 	"path/filepath"
// 	"testing"
// )

// func TestDetectFileType(t *testing.T) {
// 	tests := []struct {
// 		input    string
// 		expected string
// 	}{
// 		{"file.txt", "txt"},
// 		{"archive.tar.gz", "gz"},  // only last extension is taken
// 		{"no_extension", "unknown"},
// 		{".hiddenfile", "unknown"},
// 	}

// 	for _, tt := range tests {
// 		got := DetectFileType(tt.input)
// 		if got != tt.expected {
// 			t.Errorf("DetectFileType(%q) = %q; want %q", tt.input, got, tt.expected)
// 		}
// 	}
// }

// func TestAnalyzeFile(t *testing.T) {
// 	fileName := "test_file.txt"
// 	content := []byte("Hello World")
// 	err := os.WriteFile(fileName, content, 0644)
// 	if err != nil {
// 		t.Fatalf("Failed to create test file: %v", err)
// 	}
// 	defer os.Remove(fileName)

// 	meta, err := AnalyzeFile(fileName)
// 	if err != nil {
// 		t.Fatalf("AnalyzeFile returned error: %v", err)
// 	}

// 	if meta.Size != int64(len(content)) {
// 		t.Errorf("Expected size %d, got %d", len(content), meta.Size)
// 	}
// 	if meta.Type != "txt" {
// 		t.Errorf("Expected type \"txt\", got %q", meta.Type)
// 	}
// 	if meta.ModTime == 0 {
// 		t.Error("Expected non-zero ModTime")
// 	}
// }

// func TestAnalyzeDir(t *testing.T) {
// 	dirName := "test_dir"
// 	os.Mkdir(dirName, 0755)
// 	defer os.RemoveAll(dirName)

// 	file1 := filepath.Join(dirName, "file1.txt")
// 	file2 := filepath.Join(dirName, "file2.log")
// 	file3 := filepath.Join(dirName, "file3")

// 	os.WriteFile(file1, []byte("one"), 0644)
// 	os.WriteFile(file2, []byte("two"), 0644)
// 	os.WriteFile(file3, []byte("noext"), 0644)

// 	stats, err := AnalyzeDir(dirName)
// 	if err != nil {
// 		t.Fatalf("AnalyzeDir failed: %v", err)
// 	}

// 	if stats.FileCount != 3 {
// 		t.Errorf("Expected 3 files, got %d", stats.FileCount)
// 	}
// 	if stats.FileTypes[".txt"] != 1 {
// 		t.Errorf("Expected 1 .txt file, got %d", stats.FileTypes[".txt"])
// 	}
// 	if stats.FileTypes[".log"] != 1 {
// 		t.Errorf("Expected 1 .log file, got %d", stats.FileTypes[".log"])
// 	}
// 	if stats.FileTypes["noext"] != 1 {
// 		t.Errorf("Expected 1 file with no extension, got %d", stats.FileTypes["noext"])
// 	}
// }

// func TestAnalyzeFile_NonExistent(t *testing.T) {
// 	_, err := AnalyzeFile("nonexistent_file.txt")
// 	if err == nil {
// 		t.Error("Expected error for nonexistent file, got nil")
// 	}
// }

// func TestAnalyzeDir_InvalidPath(t *testing.T) {
// 	_, err := AnalyzeDir("/this/path/does/not/exist")
// 	if err == nil {
// 		t.Error("Expected error for invalid directory path, got nil")
// 	}
// }
