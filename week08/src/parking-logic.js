export function timeToMinutes(timeStr) {
    if (!timeStr || timeStr.trim() === "") {
        throw new Error("시간을 입력해주세요.");
    }
    const timeRegex = /^([01]\d|2[0-3]):([0-5]\d)$/;
    if (!timeRegex.test(timeStr)) {
        throw new Error("올바른 시간 형식(HH:mm)이 아닙니다.");
    }
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
}

export function calculateParkingFee(entryTimeStr, exitTimeStr) {
    const entryMinutes = timeToMinutes(entryTimeStr);
    const exitMinutes = timeToMinutes(exitTimeStr);
    
    let actualExitMinutes = exitMinutes;
    if (exitMinutes < entryMinutes) {
        actualExitMinutes += 1440; 
    }
    
    const duration = actualExitMinutes - entryMinutes;
    let fee = 0;
    
    if (duration > 30) {
        const taxableMinutes = duration - 30;
        const units = Math.ceil(taxableMinutes / 10);
        fee = units * 500;
    }
    
    fee = Math.min(fee, 20000);
    return { fee: fee, duration: duration };
}

export function formatDuration(totalMinutes) {
    const hours = Math.floor(totalMinutes / 60);
    const mins = totalMinutes % 60;
    if (hours === 0) return `${mins}분`;
    if (mins === 0) return `${hours}시간`;
    return `${hours}시간 ${mins}분`;
}

export function formatCurrency(amount) {
    return amount.toLocaleString('ko-KR');
}
