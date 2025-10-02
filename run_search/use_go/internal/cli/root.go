package cli

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"lottery_stats_simulator/run_search/go/internal/analyzer"
	"lottery_stats_simulator/run_search/go/internal/output"

	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

// flags/args - vars ____________________
var (
	catalogRoot string
	exportDir   string
	exportName  string
	games       []string
	suggestN    int
	strategy    string
	avoidLatest int

	printAll     bool
	printFreq    bool
	printUniques bool
	printSugs    bool
	noColor      bool
	htmlOut      bool
)

// root/main call  _____________________________________________________________
var rootCmd = &cobra.Command{
	Use:   "analyze",
	Short: "Analyze lottery catalog results and generate gameplay suggestions",
	Run: func(cmd *cobra.Command, args []string) {
		// Initialize writer for streaming output
		writer := bufio.NewWriter(cmd.OutOrStdout())
		defer writer.Flush()

		// ________ color functions:
		green := color.New(color.FgGreen).SprintFunc()
		yellow := color.New(color.FgYellow).SprintFunc()
		red := color.New(color.FgRed).FprintlnFunc()
		cyan := color.New(color.FgCyan).SprintFunc()

		// ________ args cli input check:
		if len(games) == 0 {
			// Default to all known games
			games = []string{"megamillion", "powerball", "lotto", "luckyday", "pick3", "pick4"}
			if !noColor {
				fmt.Fprintf(writer, "%s: no --games provided, defaulting to all (%s)\n",
					yellow("Notice"),
					strings.Join(games, ", "),
				)
			} else {
				fmt.Fprintf(writer, "Notice: no --games provided, defaulting to all (%s)\n",
					strings.Join(games, ", "),
				)
			}
			writer.Flush()
		}

		if suggestN < 0 {
			red(os.Stderr, "suggest must be non-negative")
			os.Exit(1)
		}
		if avoidLatest < 0 {
			red(os.Stderr, "avoid-latest must be non-negative")
			os.Exit(1)
		}

		validStrategies := map[string]bool{"rarest": true, "mixed": true}
		if !validStrategies[strategy] {
			red(os.Stderr, fmt.Sprintf("Invalid strategy: %s. Must be 'rarest' or 'mixed'", strategy))
			os.Exit(1)
		}

		if strings.Contains(exportDir, "..") || strings.Contains(exportName, "..") {
			red(os.Stderr, "Invalid export directory or name: relative paths not allowed")
			os.Exit(1)
		}

		// ________ set export name if none provided:
		if strings.TrimSpace(exportName) == "" {
			exportName = fmt.Sprintf("analysis_%s.json", time.Now().Format("20060102_150405"))
		}
		if !strings.HasSuffix(exportName, ".json") {
			exportName += ".json"
		}

		// ________ get full path:
		repoRoot, err := output.FindRepoRoot()
		if err != nil {
			red(os.Stderr, fmt.Sprintf("Failed to find repository root: %v", err))
			os.Exit(1)
		}
		outputDir := exportDir
		if !filepath.IsAbs(exportDir) {
			outputDir = filepath.Join(repoRoot, exportDir)
		}
		fullPath := filepath.Join(outputDir, exportName)
		if !noColor {
			fmt.Fprintf(writer, "%s: %s\n", green("Exporting results to"), fullPath)
		} else {
			fmt.Fprintf(writer, "Exporting results to: %s\n", fullPath)
		}
		writer.Flush()

		// ________ figureout the data source in or a catalog source path:
		sourcePath := catalogRoot
		if catalogRoot == "." {
			sourcePath = repoRoot
		} else {
			sourcePath, err = filepath.Abs(catalogRoot)
			if err != nil {
				red(os.Stderr, fmt.Sprintf("Failed to resolve catalog root: %v", err))
				os.Exit(1)
			}
		}

		// ________ map / normalize game list:
		selectedGameMap := make(map[string]bool)
		for _, g := range games {
			selectedGameMap[strings.ToLower(strings.TrimSpace(g))] = true
		}

		// ________ find catalog jsons:
		paths, err := analyzer.FindCatalogJSON(catalogRoot)
		if err != nil || len(paths) == 0 {
			if catalogRoot == "." {
				if !noColor {
					fmt.Fprintf(writer, "%s\n", yellow("No .jsons found at '.', searching repository root..."))
				} else {
					fmt.Fprintf(writer, "No JSONs found at '.', searching repository root...\n")
				}
				writer.Flush()
				paths, err = analyzer.FindCatalogJSON(repoRoot)
				if err != nil || len(paths) == 0 {
					red(os.Stderr, fmt.Sprintf("No .json files found in repository root: %v", err))
					os.Exit(1)
				}
			} else {
				red(os.Stderr, fmt.Sprintf("No .json files found in '%s': %v", catalogRoot, err))
				os.Exit(1)
			}
		}

		// ________ parse draw records:
		sequences, err := analyzer.LoadSequences(paths, selectedGameMap)
		if err != nil || len(sequences) == 0 {
			red(os.Stderr, fmt.Sprintf("No valid sequences found for selected games: %v", games))
			os.Exit(1)
		}
		if !noColor {
			fmt.Fprintf(writer, "%s: %d\n", green("Loaded sequences"), len(sequences))
		} else {
			fmt.Fprintf(writer, "Loaded sequences: %d\n", len(sequences))
		}
		writer.Flush()

		// ________  analyze frequency maps:
		frequencies := analyzer.BuildFrequencies(sequences)
		if !noColor {
			fmt.Fprintf(writer, "%s: %d game(s)\n", green("Frequency map built for"), len(frequencies))
		} else {
			fmt.Fprintf(writer, "Frequency map built for: %d game(s)\n", len(frequencies))
		}
		writer.Flush()

		// ________ track unique historical entries:
		originMap := analyzer.TrackOrigins(sequences)
		uniqueSequences := analyzer.UniqToSlice(originMap)
		if !noColor {
			fmt.Fprintf(writer, "%s: %d\n", green("Found unique sequence entries"), len(uniqueSequences))
		} else {
			fmt.Fprintf(writer, "Found unique sequence entries: %d\n", len(uniqueSequences))
		}
		writer.Flush()

		// ________ generate gameplay suggestions:
		suggestions, summary := analyzer.GenerateSuggestions(
			sequences,
			selectedGameMap,
			analyzer.DefaultGameLimits,
			frequencies,
			avoidLatest,
			strategy,
			suggestN,
		)

		// ________ set print flags if printAll:
		if printAll {
			printFreq = true
			printUniques = true
			printSugs = true
		}

		// ________  rich-output | optional:
		if printFreq {
			fmt.Fprintf(writer, "\n[FREQUENCY MAP]\n")

			for game, gameFreq := range frequencies {
				if !noColor {
					fmt.Fprintf(writer, "  %s → %d primary values, %d bonus values\n",
						yellow(strings.ToUpper(game)), gameFreq.TotalPrimary, gameFreq.TotalBonus)
				} else {
					fmt.Fprintf(writer, "  %s → %d primary values, %d bonus values\n",
						strings.ToUpper(game), gameFreq.TotalPrimary, gameFreq.TotalBonus)
				}

				// Show detailed breakdown for primary numbers
				fmt.Fprintf(writer, "    Primary frequencies:\n")
				for n, count := range gameFreq.Primary {
					pct := float64(count) / float64(gameFreq.TotalPrimary) * 100

					// Collect file origins
					files := []string{}
					for f, c := range gameFreq.FileOrigins[n] {
						files = append(files, fmt.Sprintf("%s:%d", f, c))
					}

					if !noColor {
						fmt.Fprintf(writer, "      %2d → %3d (%.2f%%) [%s]\n",
							n, count, pct, strings.Join(files, ", "))
					} else {
						fmt.Fprintf(writer, "      %2d → %3d (%.2f%%) [%s]\n",
							n, count, pct, strings.Join(files, ", "))
					}
				}

				// Show detailed breakdown for bonus numbers
				if len(gameFreq.Bonus) > 0 {
					fmt.Fprintf(writer, "    Bonus frequencies:\n")
					for n, count := range gameFreq.Bonus {
						pct := float64(count) / float64(gameFreq.TotalBonus) * 100

						// Collect bonus file origins
						files := []string{}
						for f, c := range gameFreq.BonusOrigins[n] {
							files = append(files, fmt.Sprintf("%s:%d", f, c))
						}

						if !noColor {
							fmt.Fprintf(writer, "      %2d → %3d (%.2f%%) [%s]\n",
								n, count, pct, strings.Join(files, ", "))
						} else {
							fmt.Fprintf(writer, "      %2d → %3d (%.2f%%) [%s]\n",
								n, count, pct, strings.Join(files, ", "))
						}
					}
				}
				writer.Flush()
			}
		}
		if printUniques {
			if !noColor {
				fmt.Fprintf(writer, "\n[UNIQUES] %s: %d\n", green("Total unique sequences"), len(uniqueSequences))
			} else {
				fmt.Fprintf(writer, "\n[UNIQUES] Total unique sequences: %d\n", len(uniqueSequences))
			}
			writer.Flush()
		}

		if printSugs {
			fmt.Fprintf(writer, "\n[SUGGESTIONS]\n")
			for _, s := range suggestions {
				// ________ format primary numbers| carry over fixed width:
				var formattedNumbers []string
				for _, num := range s.Primary {
					formattedNumbers = append(formattedNumbers, fmt.Sprintf("%-4d", num))
				}
				primaryStr := "[" + strings.Join(formattedNumbers, " ") + "]"
				bonusStr := fmt.Sprintf("+%-2d", s.Bonus)
				if !noColor {
					fmt.Fprintf(writer, "  - %s → %s %s (%s)\n",
						yellow(strings.ToUpper(s.Game)),
						cyan(primaryStr),
						cyan(bonusStr),
						s.Strategy)
				} else {
					fmt.Fprintf(writer, "  - %s → %s %s (%s)\n",
						strings.ToUpper(s.Game),
						primaryStr,
						bonusStr,
						s.Strategy)
				}
				writer.Flush()
			}
		}

		// ________ print suggestions summary:
		for game, count := range summary {
			if !noColor {
				fmt.Fprintf(writer, "%s: %d suggestions for %s\n", green("Generated"), count, game)
			} else {
				fmt.Fprintf(writer, "Generated: %d suggestions for %s\n", count, game)
			}
			writer.Flush()
		}

		// ________ convert suggestions for .json exports:
		converted := make([]output.Suggestion, 0, len(suggestions))
		for i, s := range suggestions {
			var trace []string
			if s.Notes != "" {
				trace = []string{s.Notes}
			} // ________  else trace remains nil:
			converted = append(converted, output.Suggestion{
				Game:   s.Game,
				Values: s.Primary,
				Source: s.Strategy,
				Index:  i,
				Trace:  trace,
			})
		}

		// ________ .json export:
		err = output.WriteJSON(converted, summary, sourcePath, exportDir, exportName)
		if err != nil {
			red(os.Stderr, fmt.Sprintf("Export error: %v", err))
			os.Exit(1)
		}
	},
}

// ________ call cli args:
func Execute() {
	cobra.CheckErr(rootCmd.Execute())
}

// ________ wire flags:
func init() {
	rootCmd.Flags().StringVar(&catalogRoot, "catalog-root", ".", "Root directory to search for catalog JSON files")
	rootCmd.Flags().StringVar(&exportDir, "export-dir", "analytics", "Directory to write analysis output")
	rootCmd.Flags().StringVar(&exportName, "export-json", "", "Output JSON file name (default: timestamped)")

	rootCmd.Flags().StringSliceVar(&games, "games", []string{}, "Comma-separated list of games to analyze (default: all)")
	rootCmd.Flags().IntVar(&suggestN, "suggest", 5, "Number of suggested sequences per game")
	rootCmd.Flags().StringVar(&strategy, "strategy", "rarest", "Suggestion strategy: rarest | mixed")
	rootCmd.Flags().IntVar(&avoidLatest, "avoid-latest", 0, "Avoid numbers seen in last K draws")

	rootCmd.Flags().BoolVar(&printAll, "print-all", false, "Print all results (frequencies, uniques, suggestions)")
	rootCmd.Flags().BoolVar(&printFreq, "print-freq", false, "Print frequency tables with percentages")
	rootCmd.Flags().BoolVar(&printUniques, "print-uniques", false, "Print unique sequences")
	rootCmd.Flags().BoolVar(&printSugs, "print-suggestions", false, "Print suggestions")
	rootCmd.Flags().BoolVar(&noColor, "no-color", false, "Disable colored terminal output")
	rootCmd.Flags().BoolVar(&htmlOut, "html", false, "Also export HTML report")
}
