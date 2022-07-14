import React from 'react';

import { Table } from 'antd';

import { toHHMMSS } from '../../../assets/utils';

const columns = [
    {
        title: "Timestamp",
        dataIndex: "ts",
        key: 'ts',
        render: value => new Date(value).toLocaleString('ru-RU')
    },
    {
        title: "Timer",
        dataIndex: "timer_value",
        key: 'timer_value',
        render: value => toHHMMSS(value),
    },
    {
        title: "Event",
        dataIndex: 'type',
        key: 'type',
        render: value => value ? "Stop" : "Start",
    }
]

const EventsTable = ({ events }) => {
    return (
        <Table columns={columns} dataSource={events} bordered/>
    );
};

export default React.memo(EventsTable);