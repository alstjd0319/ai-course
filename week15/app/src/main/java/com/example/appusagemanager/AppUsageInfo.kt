package com.example.appusagemanager

import android.graphics.drawable.Drawable

/**
 * 앱의 정보와 사용 통계를 담는 데이터 모델
 */
data class AppUsageInfo(
    val packageName: String,
    val appName: String,
    val icon: Drawable?,
    val totalUsageTimeMillis: Long, // 밀리초 단위 사용 시간
    val lastUsedTimeMillis: Long    // 마지막 사용 시점
)
