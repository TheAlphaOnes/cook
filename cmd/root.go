package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "cook",
	Short: "COOK  CLI tool, Swiss tool for developers",
	Long:  `COOK  CLI tool, Swiss tool for developers and platform, Powered By TheAlphaOnes`,
	Run: func(cmd *cobra.Command, args []string) {
		// Do Stuff Here
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
