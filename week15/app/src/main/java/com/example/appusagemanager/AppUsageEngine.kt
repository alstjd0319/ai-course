package com.example.appusagemanager

import android.app.usage.UsageStats
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.drawable.Drawable

/**
 * 설치된 앱 목록과 사용 통계를 결합하여 수집하는 엔진 클래스
 */
class AppUsageEngine(
    private val context: Context,
    private val packageManager: PackageManager,
    private val usageStatsManager: UsageStatsManager
) {

    /**
     * 최근 N일 동안의 데이터를 기반으로 앱 사용 정보 리스트를 가져옵니다.
     */
    fun getAppUsageList(days: Int = 7): List<AppUsageInfo> {
        val endTime = System.currentTimeMillis()
        val startTime = endTime - (days.toLong() * 24 * 60 * 60 * 1000)

        // 1. UsageStatsManager로부터 사용 통계 쿼리
        val stats: List<UsageStats> = usageStatsManager.queryUsageStats(
            UsageStatsManager.INTERVAL_DAILY,
            startTime,
            endTime
        )

        // 2. 패키지명 기반으로 UsageStats 맵 생성 (조회 속도 최적화)
        val statsMap = stats.associateBy { it.packageName }

        // 3. 설치된 모든 앱을 순회하며 통계 데이터 결합
        val installedApps = packageManager.getInstalledApplications(PackageManager.GET_META_DATA)
        
        return installedApps.mapNotNull { appInfo ->
            val packageName = appInfo.packageName
            val usageStat = statsMap[packageName]

            // 사용 기록이 아예 없는 앱은 제외하거나 0으로 처리 (여기서는 기록이 있는 앱 위주로 추출)
            // 만약 미사용 앱까지 모두 보여주고 싶다면 filter를 빼고 기본값을 0으로 설정하면 됨
            if (usageStat != null) {
                AppUsageInfo(
                    packageName = packageName,
                    appName = appInfo.loadLabel(packageManager).toString(),
                    icon = appInfo.loadIcon(packageManager),
                    totalUsageTimeMillis = usageStat.totalTimeInForeground,
                    lastUsedTimeMillis = usageStat.lastTimeUsed
                )
            } else {
                // 사용 기록이 없는 앱도 일단 포함시키고 싶다면 (기획서의 '미사용 앱 필터링'을 위해)
                // 사용 시간 0으로 세팅
                AppUsageInfo(
                    packageName = packageName,
                    appName = appInfo.loadLabel(packageManager).toString(),
                    icon = appInfo.loadIcon(packageManager),
                    totalUsageTimeMillis = 0L,
                    lastUsedTimeMillis = 0L
                )
            }
        }.sortedByDescending { it.totalUsageTimeMillis } // 기본적으로 사용 시간순 정렬
    }
}
