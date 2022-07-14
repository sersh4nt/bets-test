import React, { useEffect, useState } from "react";
import useWebSocket from 'react-use-websocket';

import { Layout, Typography, Button, Space } from 'antd';

import EventsTable from "./EventsTable";
import { toHHMMSS } from "../../assets/utils";

const { Content } = Layout;

const baseURL = 'http://localhost:8000/'
const wsURL = 'ws://localhost:8000/ws/timer/'

const IndexPage = () => {
    const [timerValue, setTimerValue] = useState(0);
    const [events, setEvents] = useState([]);
    const [isStopped, setIsStopped] = useState(true);

    const { lastJsonMessage } = useWebSocket(wsURL);

    const handlePostEvent = async () => {
        const response = await fetch(baseURL + 'api/post-event/', { method: 'POST' })
        const data = await response.json();
        setIsStopped(!data['is_running'])
    }

    useEffect(() => {
        if (!lastJsonMessage) return;
        const { events, value } = lastJsonMessage;
        setTimerValue(value);
        setEvents(events)
    }, [lastJsonMessage])

    return (
        <Content style={{ maxWidth: 1200, height: '100vh', background: '#fff', margin: 'auto', padding: 32 }}>
            <Space direction="vertical" style={{ width: '100%' }} size='large'>
                <Space>
                    <Typography>{`Timer value: ${toHHMMSS(timerValue)}`}</Typography>
                    <Button type="primary" onClick={handlePostEvent}>{isStopped ? "Start" : "Stop"}</Button>
                </Space>
                <EventsTable events={events} />
            </Space>
        </Content>
    );
}

export default IndexPage;
