package com.example.appusagemanager

import android.app.AppOpsManager
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView

class MainActivity : AppCompatActivity() {

    private lateinit var tvStatus: TextView
    private lateinit var btnPermission: Button
    private lateinit var layoutPermissionRequest: LinearLayout
    private lateinit var layoutMainContent: LinearLayout
    private lateinit var rvAppUsage: RecyclerView
    private lateinit var btnSortTime: Button
    private lateinit var btnSortRecent: Button

    private lateinit var adapter: AppUsageAdapter
    private var currentAppList = mutableListOf<AppUsageInfo>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initViews()
        setupRecyclerView()
        setupSortButtons()

        // 1. 앱 실행 시 권한 상태 확인
        checkUsageStatsPermission()

        // 2. 권한 요청 버튼 클릭 시 설정 화면으로 이동
        btnPermission.setOnClickListener {
            requestUsageStatsPermission()
        }
    }

    private fun initViews() {
        tvStatus = findViewById(R.id.tv_status)
        btnPermission = findViewById(R.id.btn_permission)
        layoutPermissionRequest = findViewById(R.id.layout_permission_request)
        layoutMainContent = findViewById(R.id.layout_main_content)
        rvAppUsage = findViewById(R.id.rv_app_usage)
        btnSortTime = findViewById(R.id.btn_sort_time)
        btnSortRecent = findViewById(R.id.btn_sort_recent)
    }

    private fun setupRecyclerView() {
        adapter = AppUsageAdapter(currentAppList) { appInfo ->
            // TODO: 4단계 - 앱 상세 정보 페이지 이동 구현
        }
        rvAppUsage.layoutManager = LinearLayoutManager(this)
        rvAppUsage.adapter = adapter
    }

    private fun setupSortButtons() {
        btnSortTime.setOnClickListener {
            sortListByTime()
        }
        btnSortRecent.setOnClickListener {
            sortListByRecent()
        }
    }

    /**
     * 사용자의 Usage Stats(앱 사용 통계) 권한 보유 여부를 확인합니다.
     */
    private fun checkUsageStatsPermission() {
        val appOps = getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
        val mode = appOps.checkOpNoThrow(
            AppOpsManager.OPSTR_GET_USAGE_STATS,
            android.os.Process.myUid(),
            packageName
        )

        if (mode == AppOpsManager.MODE_ALLOWED) {
            showMainContent()
        } else {
            showPermissionRequest()
        }
    }

    private fun showPermissionRequest() {
        layoutPermissionRequest.visibility = View.VISIBLE
        layoutMainContent.visibility = View.GONE
        tvStatus.text = "앱 사용 기록을 보기 위해 권한 승인이 필요합니다."
        btnPermission.visibility = View.VISIBLE
    }

    private fun showMainContent() {
        layoutPermissionRequest.visibility = View.GONE
        layoutMainContent.visibility = View.VISIBLE
        
        // 2단계 데이터 로드 시뮬레이션 (실제로는 Engine에서 데이터를 가져옴)
        loadMockData()
    }

    private fun loadMockData() {
        // 테스트용 더미 데이터
        currentAppList.clear()
        currentAppList.add(AppUsageInfo("com.example.app1", "App One", null, 3600000, 1700000000000L))
        currentAppList.add(AppUsageInfo("com.example.app2", "App Two", null, 1800000, 1700010000000L))
        currentAppList.add(AppUsageInfo("com.example.app3", "App Three", null, 0, 1700020000000L))
        currentAppList.add(AppUsageInfo("com.example.app4", "App Four", null, 7200000, 1690000000000L))
        
        adapter.updateData(currentAppList)
    }

    private fun sortListByTime() {
        // 사용 시간 내림차순 (많이 쓴 순)
        currentAppList.sortByDescending { it.totalUsageTimeMillis }
        adapter.updateData(currentAppList)
    }

    private fun sortListByRecent() {
        // 최근 사용 시점 내림차순 (최근에 쓴 순)
        currentAppList.sortByDescending { it.lastUsedTimeMillis }
        adapter.updateData(currentAppList)
    }

    /**
     * 시스템의 '사용정보 접근 권한' 설정 화면으로 사용자를 이동시킵니다.
     */
    private fun requestUsageStatsPermission() {
        val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
        startActivity(intent)
    }

    override fun onResume() {
        super.onResume()
        checkUsageStatsPermission()
    }
}
