package com.example.appusagemanager

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import java.util.Locale

class AppUsageAdapter(
    private var appList: List<AppUsageInfo>,
    private val onItemClick: (AppUsageInfo) -> Unit
) : RecyclerView.Adapter<AppUsageAdapter.AppUsageViewHolder>() {

    class AppUsageViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val ivIcon: ImageView = view.findViewById(R.id.iv_app_icon)
        val tvName: TextView = view.findViewById(R.id.tv_app_name)
        val tvTime: TextView = view.findViewById(R.id.tv_usage_time)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AppUsageViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_app_usage, parent, false)
        return AppUsageViewHolder(view)
    }

    override fun onBindViewHolder(holder: AppUsageViewHolder, position: Int) {
        val app = appList[position]
        holder.tvName.text = app.appName
        holder.ivIcon.setImageDrawable(app.icon)
        holder.tvTime.text = formatTime(app.totalUsageTimeMillis)

        holder.itemView.setOnClickListener {
            onItemClick(app)
        }
    }

    override fun getItemCount(): Int = appList.size

    /**
     * 밀리초(ms) 단위를 "X시간 Y분" 또는 "X분" 형태로 변환합니다.
     */
    private fun formatTime(millis: Long): String {
        if (millis <= 0) return "사용 기록 없음"
        
        val totalMinutes = millis / (1000 * 60)
        val hours = totalMinutes / 60
        val minutes = totalMinutes % 60

        return if (hours > 0) {
            String.format(Locale.getDefault(), "%d시간 %d분", hours, minutes)
        } else {
            String.format(Locale.getDefault(), "%d분", minutes)
        }
    }

    fun updateData(newList: List<AppUsageInfo>) {
        this.appList = newList
        notifyDataSetChanged()
    }
}
