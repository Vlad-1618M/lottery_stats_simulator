package diff

import "testing"

func TestDiffTextNoChange(t *testing.T) {
	changed, result := DiffText("hello", "hello")
	if changed {
		t.Error("Expected no change, but got change")
	}
	if result != "" {
		t.Errorf("Expected empty diff, got: %q", result)
	}
}

func TestDiffTextNewFile(t *testing.T) {
	changed, result := DiffText("", "new content")
	if !changed {
		t.Error("Expected change for new file, got no change")
	}
	if result != "new content" {
		t.Errorf("Expected full new content, got: %q", result)
	}
}

func TestDiffTextAppended(t *testing.T) {
	changed, result := DiffText("hello", "hello world")
	if !changed {
		t.Error("Expected change for appended content, got no change")
	}
	if result != " world" {
		t.Errorf("Expected appended diff ' world', got: %q", result)
	}
}

func TestDiffTextShorterOrDifferent(t *testing.T) {
	changed, result := DiffText("hello world", "short")
	if !changed {
		t.Error("Expected change for shorter content, got no change")
	}
	if result != "short" {
		t.Errorf("Expected full new content 'short', got: %q", result)
	}
}

func TestDiffText_Deletion(t *testing.T) {
	oldText := "hello world"
	newText := "hello"

	changed, result := DiffText(oldText, newText)
	if !changed {
		t.Error("Expected change when text is deleted, got no change")
	}
	if result != newText {
		t.Errorf("Expected entire new text after deletion, got: %q", result)
	}
}