package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var versionCMD = &cobra.Command{
	Use:   "version",
	Short: "cook cli version",
	Long:  `get the cook cli version`,
	Run: func(cmd *cobra.Command, args []string) {
		// Do Stuff Here
		versionBar()
	},
}

func versionBar() {
	fmt.Println("COOK version 1.0.0-alpha")
}

func init() {
	rootCmd.AddCommand(versionCMD)
}
