// internal/diff/diff.go
package diff

// DiffText compares old and new content.
// If old is empty (new file), returns entire new content.
// If content was appended, returns only the appended part.
// Otherwise, returns full new content.
func DiffText(oldText, newText string) (bool, string) {
	if oldText == newText {
		return false, ""
	}

	// If old is empty (new file), show full content
	if oldText == "" {
		return true, newText
	}

	// If new text is longer → appended
	if len(newText) > len(oldText) {
		return true, newText[len(oldText):]
	}

	// Fallback: full content
	return true, newText
}

// ==============================================================================
// // internal/diff/diff.go
// package diff

// import (
// 	"strings"
// )

// // DiffText compares old and new content and returns true if they differ.
// // It also returns the new appended part if detected.
// func DiffText(oldContent, newContent string) (bool, string) {
// 	if oldContent == newContent {
// 		return false, ""
// 	}

// 	oldLines := strings.Split(oldContent, "\n")
// 	newLines := strings.Split(newContent, "\n")

// 	// If new content has more lines, return only the new part
// 	if len(newLines) > len(oldLines) {
// 		added := strings.Join(newLines[len(oldLines):], "\n")
// 		return true, added
// 	}

// 	// Otherwise return the full new content
// 	return true, newContent
// }
