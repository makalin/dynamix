"""
Export Tools - Various export formats for analysis results
Supports multiple formats: JSON, CSV, XML, M3U, Rekordbox, Traktor, etc.
"""

import json
import csv
import os
from typing import List, Dict, Optional
from datetime import datetime
import xml.etree.ElementTree as ET


class ExportTools:
    """Tools for exporting analysis results in various formats"""
    
    @staticmethod
    def export_to_json(data: Dict, output_path: str, indent: int = 2):
        """Export data to JSON format"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, default=str, ensure_ascii=False)
        print(f"✅ Exported to JSON: {output_path}")
    
    @staticmethod
    def export_to_csv(data: List[Dict], output_path: str):
        """Export list of dictionaries to CSV"""
        if not data:
            print("⚠️  No data to export")
            return
        
        fieldnames = data[0].keys()
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Exported to CSV: {output_path}")
    
    @staticmethod
    def export_to_m3u(playlist: List[Dict], output_path: str, extended: bool = True):
        """
        Export playlist to M3U format
        Supports both standard and extended M3U formats
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            if extended:
                f.write("#EXTM3U\n")
            
            for track in playlist:
                if extended:
                    duration = track.get('duration', 0)
                    title = track.get('filename', track.get('file_path', 'Unknown'))
                    f.write(f"#EXTINF:{int(duration)},{title}\n")
                
                file_path = track.get('file_path', track.get('filename', ''))
                f.write(f"{file_path}\n")
        
        print(f"✅ Exported to M3U: {output_path}")
    
    @staticmethod
    def export_to_rekordbox_xml(playlist: List[Dict], output_path: str, playlist_name: str = "DynaMix Playlist"):
        """
        Export playlist to Rekordbox XML format
        """
        root = ET.Element("DJ_PLAYLISTS")
        root.set("Version", "1.0.0")
        
        collection = ET.SubElement(root, "COLLECTION")
        
        tracks_elem = ET.SubElement(collection, "TRACKS")
        
        for i, track in enumerate(playlist):
            track_elem = ET.SubElement(tracks_elem, "TRACK")
            track_elem.set("TrackID", str(i + 1))
            
            file_path = track.get('file_path', track.get('filename', ''))
            track_elem.set("Location", f"file://localhost{os.path.abspath(file_path)}")
            
            filename = os.path.basename(file_path)
            ET.SubElement(track_elem, "Name").text = filename
            
            if 'bpm' in track:
                ET.SubElement(track_elem, "AverageBpm").text = str(int(track['bpm']))
            
            if 'key' in track:
                ET.SubElement(track_elem, "Tonality").text = track['key']
            
            if 'duration' in track:
                ET.SubElement(track_elem, "TotalTime").text = str(int(track['duration'] * 1000))
        
        # Create playlist
        playlists = ET.SubElement(root, "PLAYLISTS")
        node = ET.SubElement(playlists, "NODE")
        node.set("Type", "1")
        node.set("Name", "ROOT")
        
        sub_node = ET.SubElement(node, "NODE")
        sub_node.set("Name", playlist_name)
        
        playlist_elem = ET.SubElement(sub_node, "PLAYLIST")
        playlist_elem.set("Type", "1")
        playlist_elem.set("Name", playlist_name)
        
        tracks = ET.SubElement(playlist_elem, "TRACKS")
        for i in range(len(playlist)):
            track_ref = ET.SubElement(tracks, "TRACK")
            track_ref.set("Key", str(i + 1))
        
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ Exported to Rekordbox XML: {output_path}")
    
    @staticmethod
    def export_to_traktor_nml(playlist: List[Dict], output_path: str, playlist_name: str = "DynaMix Playlist"):
        """
        Export playlist to Traktor NML format
        """
        root = ET.Element("NML")
        root.set("VERSION", "19")
        
        collection = ET.SubElement(root, "COLLECTION")
        collection.set("ENTRIES", str(len(playlist)))
        
        for i, track in enumerate(playlist):
            entry = ET.SubElement(collection, "ENTRY")
            entry.set("MODIFIED_DATE", str(int(datetime.now().timestamp())))
            entry.set("MODIFIED_TIME", str(int(datetime.now().timestamp())))
            
            location = ET.SubElement(entry, "LOCATION")
            file_path = track.get('file_path', track.get('filename', ''))
            location.set("DIR", os.path.dirname(os.path.abspath(file_path)))
            location.set("FILE", os.path.basename(file_path))
            location.set("VOLUME", "volume")
            
            info = ET.SubElement(entry, "INFO")
            info.set("BITRATE", "320")
            info.set("RANKING", "0")
            info.set("PLAYCOUNT", "0")
            
            if 'duration' in track:
                info.set("PLAYTIME", str(int(track['duration'])))
            
            if 'bpm' in track:
                tempo = ET.SubElement(entry, "TEMPO")
                tempo.set("BPM", str(int(track['bpm'] * 100)))
                tempo.set("BPM_QUALITY", "100")
            
            if 'key' in track:
                musical_key = ET.SubElement(entry, "MUSICAL_KEY")
                musical_key.set("VALUE", track['key'])
        
        # Create playlist
        playlists = ET.SubElement(root, "PLAYLISTS")
        node = ET.SubElement(playlists, "NODE")
        node.set("TYPE", "PLAYLIST")
        node.set("NAME", playlist_name)
        
        playlist = ET.SubElement(node, "PLAYLIST")
        playlist.set("ENTRIES", str(len(playlist)))
        playlist.set("TYPE", "LIST")
        playlist.set("UUID", "dynamix-playlist")
        
        for i in range(len(playlist)):
            entry_ref = ET.SubElement(playlist, "ENTRY")
            entry_ref.set("PRIMARYKEY", str(i + 1))
        
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ Exported to Traktor NML: {output_path}")
    
    @staticmethod
    def export_dj_notes_batch(notes_list: List[Dict], output_dir: str):
        """
        Export multiple DJ notes to text files
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for note_data in notes_list:
            filename = note_data.get('filename', 'unknown')
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}_dj_notes.txt")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(note_data.get('notes', ''))
        
        print(f"✅ Exported {len(notes_list)} DJ notes to {output_dir}")
    
    @staticmethod
    def export_compatibility_matrix(compatibility_data: Dict, output_path: str, format: str = 'csv'):
        """
        Export compatibility matrix to file
        """
        if format == 'csv':
            rows = []
            for key, data in compatibility_data.items():
                rows.append({
                    'track1_index': data.get('track1_index', ''),
                    'track2_index': data.get('track2_index', ''),
                    'bpm_compatibility': data.get('compatibility', {}).get('bpm_compatibility', 0),
                    'key_compatibility': data.get('compatibility', {}).get('key_compatibility', 0),
                    'energy_compatibility': data.get('compatibility', {}).get('energy_compatibility', 0),
                    'overall_score': data.get('compatibility', {}).get('overall_score', 0),
                    'bpm_difference': data.get('bpm_difference', 0),
                    'energy_difference': data.get('energy_difference', 0)
                })
            
            ExportTools.export_to_csv(rows, output_path)
        elif format == 'json':
            ExportTools.export_to_json(compatibility_data, output_path)
        else:
            print(f"⚠️  Unsupported format: {format}")
    
    @staticmethod
    def export_analysis_report(analysis_data: Dict, output_path: str, format: str = 'txt'):
        """
        Export comprehensive analysis report
        """
        if format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("DYNAMIX ANALYSIS REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Write track information
                if 'track1' in analysis_data:
                    f.write("TRACK 1:\n")
                    f.write("-" * 40 + "\n")
                    track1 = analysis_data['track1']
                    for key, value in track1.items():
                        if key != 'sections' and key != 'drops':
                            f.write(f"  {key}: {value}\n")
                    f.write("\n")
                
                if 'track2' in analysis_data:
                    f.write("TRACK 2:\n")
                    f.write("-" * 40 + "\n")
                    track2 = analysis_data['track2']
                    for key, value in track2.items():
                        if key != 'sections' and key != 'drops':
                            f.write(f"  {key}: {value}\n")
                    f.write("\n")
                
                # Write compatibility
                if 'compatibility' in analysis_data:
                    f.write("COMPATIBILITY:\n")
                    f.write("-" * 40 + "\n")
                    compat = analysis_data['compatibility']
                    for key, value in compat.items():
                        f.write(f"  {key}: {value}\n")
                    f.write("\n")
                
                # Write mix suggestions
                if 'mix_suggestions' in analysis_data:
                    f.write("MIX SUGGESTIONS:\n")
                    f.write("-" * 40 + "\n")
                    suggestions = analysis_data['mix_suggestions']
                    for key, value in suggestions.items():
                        f.write(f"  {key}: {value}\n")
            
            print(f"✅ Exported analysis report: {output_path}")
        else:
            ExportTools.export_to_json(analysis_data, output_path)

