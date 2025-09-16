package analyzer

import (
	"time"
)

// _____ parseTime supports both ISO (catalog) and "Jan 2, 2006" formats:| return zero time if parsing fails
func parseTime(s string) time.Time {
	if t, err := time.Parse(time.RFC3339, s); err == nil {
		return t
	}
	if t, err := time.Parse("Jan 2, 2006", s); err == nil {
		return t
	}
	return time.Time{}
}
