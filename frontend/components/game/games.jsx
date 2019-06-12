import React, { useState, useLayoutEffect } from 'react';

const weekdays = {
    0: "Sun",
    1: "Mon",
    2: "Tue",
    3: "Wed",
    4: "Thu",
    5: "Fri",
    6: "Sat"
};

export default function Games() {
    const today = new Date();
    const [date, setdate] = useState(today);
    const [offset, setoffset] = useState(0);

    const startDate = new Date(date);
    const endDate = new Date(date);
    const dates = [];

    
    // useLayoutEffect(() => {
        startDate.setDate(date.getDate() - 3);
        endDate.setDate(date.getDate() + 3);
        // debugger;
    // });
    
    let current = startDate;

    while (current <= endDate) {
        let datesClasses = "dates";
        if (current.toDateString() === date.toDateString())
            datesClasses += " selected-date";
        dates.push(
            <div className={datesClasses}
                onClick={() => setdate(current)}>
                <div className="weekday">{weekdays[current.getDay()]}</div>
                <div className="month-date">{current.getDate()}</div>
            </div>
        );
        current.setDate(current.getDate()+1);
    }

    return (
        <div className="container is-flexed">
            <div className="games-title">Games</div>
            <div className="date-panel">
                <div className="date-range">
                    {startDate.toDateString()} - {endDate.toDateString()}
                </div>
                <div className="date-selector">
                    <div className="arrow-container"
                        onClick={() => setoffset(offset-1)}>
                        <div className="left-arrow"></div>
                    </div>
                    {dates}
                    <div className="arrow-container"
                        onClick={() => setoffset(offset-1)}>
                        <div className="right-arrow"></div>       
                    </div>
                </div>
            </div>
        </div>
    );
}
