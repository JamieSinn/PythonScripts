package main

import (
	"fmt"
	"log"

	"strings"

	"strconv"

	"github.com/CarlColglazier/tba"
)

const (
	VERSION = "0.1.0"
)

var (
	TBA tba.Client
)

func main() {
	tba, err := tba.Init("1334", "districtscraper", VERSION)
	TBA = tba
	if err != nil {
		log.Fatal(err)
	}
	getNonDistrictTeams()
}

func getNonDistrictTeams() []tba.Team {
	var ret []tba.Team
	teams, err := TBA.GetDistrictTeams("ont", 2017)
	if err != nil {
		panic(err)
	}

	for _, team := range teams {
		teamEvents, err := TBA.GetTeamEvents(team.TeamNumber, 2017)

		if err != nil {
			panic(err)
		}

		for _, event := range teamEvents {
			if strings.Contains(event.EventCode, "2017on") || event.EventType != 0 {
				continue
			}
			fmt.Println(strconv.Itoa(team.TeamNumber) + " is attending: " + event.Name + " - " + strconv.Itoa(event.EventType))
			awards, err := TBA.GetTeamEventAwards(team.TeamNumber, event.EventCode)
			if err != nil {
				fmt.Println(strconv.Itoa(team.TeamNumber) + " has not won awards at " + event.Name)
				continue
			}
			for _, award := range awards {
				switch award.AwardType {
				case 0:
				case 9:
				case 10:
				case 1:
					fmt.Println(strconv.Itoa(team.TeamNumber) + " has a qualifying award to champs. - " + award.Name)
					ret = append(ret, team)
					break
				default:
					fmt.Println(strconv.Itoa(team.TeamNumber) + " does not qualify with: " + award.Name)
				}
			}

		}

	}
	return ret
}
