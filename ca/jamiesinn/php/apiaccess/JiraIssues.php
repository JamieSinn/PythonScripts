<?php

class JiraIssues
{
    public function __construct()
    {

    }

    private function getIssues($jql)
    {
        $result = [];
        $path = "http://api:api@ws2012-03.sinn.lan/jira/rest/api/2/search?jql=" . $jql;
        $issues = json_decode(file_get_contents($path), true)['issues'];
        foreach ($issues as $issue)
        {
            $key = $issue["key"];
            array_push($result, $key);
        }
        sort($result, SORT_NATURAL | SORT_FLAG_CASE);
        return $result;
    }

    private function getSCEAIssues()
    {
        return self::getIssues("cf%5B10100%5D%20in%20(ps4%2C%20psvr)");
    }

    private function getNintendoIssues()
    {
        return self::getIssues("");
    }

    private function getMicrosoftIssues()
    {
        return self::getIssues("");
    }

    public static function echoIssues()
    {
        foreach (self::getSCEAIssues() as $issue)
        {
            echo $issue;
        }
    }

    public function getIssuesAsList($type)
    {
        $result = "";
        if ($type == "")
        {
            $result = "<li class = \"list-group-item\">No Issues!</li>";
            return $result;
        }
        switch ($type)
        {
            case "scea":
                foreach (self::getSCEAIssues() as $issue)
                {
                    $result .= "<li class=\"list-group-item\"><a href=\"http://ws2012-03.sinn.lan/jira/browse/" . $issue . "\">" . $issue . "</a></li>";
                }
                break;
            default:
                break;
        }
        return $result;
    }
}
