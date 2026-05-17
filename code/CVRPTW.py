def solve_cvrptw_detailed():
    # Thông số từ tài liệu
    COST_PER_KM = 186.2  # Rp/km
    VEHICLE_CAPACITY = 15  # Giả định tải trọng xe
    AVG_SPEED = 0.4  # km/phút (tương đương ~24km/h để phù hợp thời gian trong Table 2)

    # Dữ liệu khách hàng (Id, Quãng đường từ X, Nhu cầu, Giờ mở, Giờ đóng)
    # Dựa trên Table 1 & 2
    customers = [
        {'id': 'A', 'dist_x': 2.5, 'demand': 5, 'ready': 0,  'due': 30},
        {'id': 'B', 'dist_x': 2.9, 'demand': 6, 'ready': 10, 'due': 40},
        {'id': 'C', 'dist_x': 2.9, 'demand': 4, 'ready': 5,  'due': 25},
        {'id': 'D', 'dist_x': 3.3, 'demand': 5, 'ready': 20, 'due': 60},
        {'id': 'E', 'dist_x': 6.2, 'demand': 8, 'ready': 10, 'due': 50},
        {'id': 'F', 'dist_x': 2.3, 'demand': 3, 'ready': 0,  'due': 20},
    ]

    unvisited = customers[:]
    fleet_data = []

    while unvisited:
        route = ['X']
        current_node_dist = 0
        current_time = 0
        current_load = 0
        route_distance = 0
        
        while unvisited:
            best_candidate = None
            min_dist = float('inf')

            for c in unvisited:
                # Tính khoảng cách tương đối giữa các điểm
                dist_to_c = abs(c['dist_x'] - current_node_dist)
                arrival_time = current_time + (dist_to_c / AVG_SPEED)

                # Kiểm tra ràng buộc Tải trọng và Cửa sổ thời gian
                if (current_load + c['demand'] <= VEHICLE_CAPACITY and 
                    arrival_time <= c['due']):
                    if dist_to_c < min_dist:
                        min_dist = dist_to_c
                        best_candidate = c

            if best_candidate:
                dist_to_c = abs(best_candidate['dist_x'] - current_node_dist)
                route_distance += dist_to_c
                arrival_time = current_time + (dist_to_c / AVG_SPEED)
                
                # Cập nhật thời gian (nếu đến sớm thì phải đợi đến 'ready')
                current_time = max(arrival_time, best_candidate['ready'])
                current_load += best_candidate['demand']
                current_node_dist = best_candidate['dist_x']
                
                route.append(best_candidate['id'])
                unvisited.remove(best_candidate)
            else:
                break
        
        # Quay về Depot X
        dist_back = current_node_dist
        route_distance += dist_back
        current_time += (dist_back / AVG_SPEED)
        route.append('X')
        
        fleet_data.append({
            'route': route,
            'distance': round(route_distance, 2),
            'time': round(current_time, 2),
            'cost': round(route_distance * COST_PER_KM, 2)
        })

    # Hiển thị kết quả theo phong cách báo cáo[cite: 1]
    print(f"{'STT':<5} | {'Lộ trình':<20} | {'Quãng đường':<15} | {'Thời gian':<12} | {'Chi phí (Rp)'}")
    print("-" * 75)
    total_all_dist = 0
    total_all_cost = 0
    
    for i, data in enumerate(fleet_data):
        print(f"Xe {i+1:<2} | {' -> '.join(data['route']):<20} | {data['distance']:>8} km | {data['time']:>7} phút | {data['cost']:>10}")
        total_all_dist += data['distance']
        total_all_cost += data['cost']
        
    print("-" * 75)
    print(f"TỔNG CỘNG: Quãng đường = {total_all_dist:.2f} km | Chi phí = {total_all_cost:.2f} Rp")

solve_cvrptw_detailed()