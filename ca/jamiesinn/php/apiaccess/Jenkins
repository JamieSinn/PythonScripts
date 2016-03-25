<?php

class Jenkins
{
    private function getJobJSON($job, $build = "lastBuild")
    {
        if($build == "" || $build == null)
            $build = "lastBuild";
        $url = "http://ws2012-03.sinn.lan/jenkins/job/" . $job . "/" . $build . "/api/json";
        return json_decode(file_get_contents($url), true);
    }

    public function getJobLatestResult($job)
    {
        return $this->getJobResult($job, null);
    }

    public function getJobResult($job, $build)
    {
        return $this->getJobJSON($job, $build)['result'];
    }
}
