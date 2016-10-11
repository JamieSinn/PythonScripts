package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"
)

func main() {
	args := os.Args[1:]
	if len(args) < 2 {
		fmt.Println("Usage: ./voting <path to votes.log> <path to output file>")
		return
	}
	fmt.Println("Getting votes for " + time.Now().AddDate(0, -1, 0).Month().String() + " " + strconv.Itoa(time.Now().Year()))
	currentVotes := stripCurrentVotes(args[0])
	stripped := stripPlayer(currentVotes)
	top10 := getTop10(stripped)
	writeTop10(top10, args[1])
	fmt.Println("Done! Please see " + args[1])
}

func getTop10(votes []string) VoteList {
	count := make(map[string]int)
	for _, str := range votes {
		count[str]++
	}
	vl := make(VoteList, len(count))
	i := 0
	for player, votes := range count {
		if player == "" {
			continue
		}
		vl[i] = Vote{player, votes}
		i++
	}
	sort.Sort(sort.Reverse(vl))
	vl = vl[:10]
	return vl
}

func writeTop10(votes VoteList, output string) {
	forumpost := "[SIZE=3][FONT=Arial][COLOR=rgb(153, 255, 204)]Congratulations to all our %s voting winnners!\n" +
		"%s Top Prizes: 5/5/5/5/4/4/4/3/3/2 Event Tokens + Voting Medal!\n" +
		"[/COLOR][/FONT][/SIZE]\n"

	f, err := os.Create(output)
	check(err)
	defer f.Close()
	fmt.Print(votes)
	writer := bufio.NewWriter(f)
	defer writer.Flush()
	writer.WriteString(forumpost)
	for i := range votes {
		writer.WriteString("@" + votes[i].Player + "\n")
	}
	writer.WriteString("[USERGROUP=19]@Server Admin[/USERGROUP] - Please update the Event Tokens thread.")
	writer.WriteString("\n\n")
	medalList := ""
	for i := range votes {
		medalList += votes[i].Player + ","
	}
	writer.WriteString(medalList)
	writer.WriteString("\n\n")

	for i := range votes {
		writer.WriteString(votes[i].Player + ":" + strconv.Itoa(votes[i].Votes) + "\n")
	}

}

func stripPlayer(votes []string) []string {
	result := make([]string, len(votes))
	pregex, err := regexp.Compile("username:.* a")
	check(err)
	for _, line := range votes {
		player := pregex.FindString(line)
		player = strings.Replace(strings.Replace(player, " a", "", -1), "username:", "", -1)
		result = append(result, player)

	}
	return result
}

func stripCurrentVotes(votefile string) []string {
	votes := make([]string, 10000)
	file, err := os.Open(votefile)
	check(err)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	timestampStrip, _ := regexp.Compile("timeStamp:\\d+")

	for scanner.Scan() {
		_timestamp, err := strconv.ParseInt(strings.Replace(timestampStrip.FindString(scanner.Text()), "timeStamp:", "", -1), 10, 64)

		check(err)
		timestamp := time.Unix(_timestamp, 0)

		if timestamp.Year() > time.Now().Year() {
			continue
		}

		if time.Now().Year() == timestamp.Year() && time.Now().AddDate(0, -1, 0).Month() == timestamp.Month() {
			votes = append(votes, scanner.Text())
		}
	}
	check(scanner.Err())
	return votes
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

// Vote - because maps can't be sorted by default.
type Vote struct {
	Player string
	Votes  int
}

// VoteList is a list of Votes
type VoteList []Vote

func (v VoteList) Len() int           { return len(v) }
func (v VoteList) Less(i, j int) bool { return v[i].Votes < v[j].Votes }
func (v VoteList) Swap(i, j int)      { v[i], v[j] = v[j], v[i] }
