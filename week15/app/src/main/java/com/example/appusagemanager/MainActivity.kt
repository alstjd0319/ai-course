package com.example.appusagemanager

import android.app.AppOpsManager
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var tvStatus: TextView
    private lateinit var btnPermission: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvStatus = findViewById(R.id.tv_status)
        btnPermission = findViewById(R.id.btn_permission)

        // 1. 앱 실행 시 권한 상태 확인
        checkUsageStatsPermission()

        // 2. 버튼 클릭 시 설정 화면으로 이동
        btnPermission.setOnClickListener {
            requestUsageStatsPermission()
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
            // 권한이 있으면 메시지 변경 (실제로는 여기서 2단계로 넘어가 앱 리스트를 보여줘야 함)
            tvStatus.text = "권한이 승인되었습니다! (2단계 준비 완료)"
            btnPermission.visibility = android.view.View.GONE
        } else {
            // 권한이 없으면 안내 문구 유지
            tvStatus.text = "앱 사용 기록을 보기 위해 권한 승인이 필요합니다."
            btnPermission.visibility = android.view.View.VISIBLE
        }
    }

    /**
     * 시스템의 '사용정보 접근 권한' 설정 화면으로 사용자를 이동시킵니다.
     */
    private fun requestUsageStatsPermission() {
        val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
        startActivity(intent)
    }

    /**
     * 사용자가 설정에서 돌아왔을 때 권한 상태를 다시 확인하기 위해 호출됩니다.
     */
    override fun onResume() {
        super.onResume()
        checkUsageStatsPermission()
    }
}
