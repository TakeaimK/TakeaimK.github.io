
import sys
import os
import torch
import soundfile as sf
import re
from datetime import datetime
from qwen_tts import Qwen3TTSModel

# -----------------------------------------------------------------------------
# [초기 설정] GPU 및 FlashAttention 설정
# -----------------------------------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32
attn_impl = "eager"

if device == "cuda":
    try:
        import flash_attn
        attn_impl = "flash_attention_2"
    except ImportError:
        print("⚠️ FlashAttention이 설치되지 않아 'eager' 모드로 실행합니다.")

# -----------------------------------------------------------------------------
# [모델 경로 설정]
# -----------------------------------------------------------------------------
MODELS = {
    "custom": "/mnt/c/Users/csj76/models/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    "design": "/mnt/c/Users/csj76/models/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    "clone": "/mnt/c/Users/csj76/models/Qwen/Qwen3-TTS-12Hz-1.7B-Base"
}

def load_model(path, model_name_for_log):
    print(f"\n[{model_name_for_log}] 모델 로딩 중... ({path})")
    return Qwen3TTSModel.from_pretrained(
        path,
        device_map="auto",
        dtype=dtype,
        attn_implementation=attn_impl
    )

def get_output_filename(type_str, identifier):
    """
    파일명 생성 규칙: output-<type>-<identifier>-<YYMMDDHHMM>.wav
    - identifier: 공백 및 특수문자는 '_'로 치환
    - timestamp: 현재 시간
    """
    # 1. Identifier 정제 (파일명에 사용할 수 없는 문자 및 공백, 특수문자 치환)
    # 한글, 영문, 숫자, 언더바, 하이픈을 제외한 모든 문자를 '_'로 변경
    clean_identifier = re.sub(r'[^가-힣a-zA-Z0-9_\-]', '_', str(identifier))
    # 연속된 언더바는 하나로 줄임
    clean_identifier = re.sub(r'_+', '_', clean_identifier)
    
    # 2. 날짜 포맷 (YYMMDDHHMM)
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    
    return f"output-{type_str}-{clean_identifier}-{timestamp}.wav"

# -----------------------------------------------------------------------------
# [기능 구현]
# -----------------------------------------------------------------------------

def run_custom_voice(text, speaker):
    """
    1. CustomVoice: 프리셋 화자 사용
    """
    model = load_model(MODELS["custom"], "CustomVoice")
    
    # 기본 instruct (필요하다면 상수로 빼거나 인자로 받을 수 있음)
    default_instruct = "차분하고 전문적인 뉴스 앵커 톤으로(Speak in a calm and professional news anchor tone)"
    
    print(f"🎙️ 생성 중: '{text}' (Speaker: {speaker})")
    
    wavs, sr = model.generate_custom_voice(
        text=text,
        language="Korean",
        speaker=speaker,
        instruct=default_instruct
    )
    
    # output-custom_voice-<Speaker>-<Date>.wav
    output_filename = get_output_filename("custom_voice", speaker)
    
    sf.write(output_filename, wavs[0], sr)
    print(f"✅ 완료: {output_filename}")

def run_voice_design(text, instruct):
    """
    2. VoiceDesign: 목소리 묘사 사용
    """
    model = load_model(MODELS["design"], "VoiceDesign")
    
    print(f"🎙️ 생성 중: '{text}'")
    print(f"✨ 목소리 묘사: {instruct}")
    
    wavs, sr = model.generate_voice_design(
        text=text,
        language="Korean",
        instruct=instruct
    )
    
    # output-voice_design-<Instruct앞10글자>-<Date>.wav
    # instruct가 길 수 있으므로 앞 10글자만 사용
    short_instruct = instruct[:10]
    output_filename = get_output_filename("voice_design", short_instruct)
    
    sf.write(output_filename, wavs[0], sr)
    print(f"✅ 완료: {output_filename}")

def run_voice_clone(text, ref_audio_path, ref_text=None):
    """
    3. VoiceClone: 목소리 복제
    """
    model = load_model(MODELS["clone"], "VoiceClone")
    
    # ref_text가 제공되지 않았을 경우 (CLI 모드 등에서)
    if not ref_text:
        print("\nℹ️  참조 오디오의 텍스트(Transcript)가 입력되지 않았습니다.")
        ref_text = input("   복제 품질을 위해 참조 오디오의 내용을 입력해주세요 (모르면 Enter): ").strip()
        if not ref_text:
            print("⚠️  Warning: 참조 텍스트 없이 진행합니다. 품질이 저하될 수 있습니다.")
            # 텍스트가 꼭 필요하다면 임의의 값이나 에러 처리가 필요할 수 있습니다.
            # 여기서는 빈 문자열이나 플레이스홀더를 사용하여 진행 시도
            ref_text = "The quick brown fox jumps over the lazy dog." 
    
    print(f"🎙️ 생성 중: '{text}'")
    print(f"🔊 참조 파일: {ref_audio_path}")
    
    wavs, sr = model.generate_voice_clone(
        text=text,
        language="Korean",
        ref_audio=ref_audio_path,
        ref_text=ref_text
    )
    
    # output-voice_clone-<RefFileName>-<Date>.wav
    # 경로에서 파일명 추출 (확장자 제외)
    base_name = os.path.basename(ref_audio_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    
    output_filename = get_output_filename("voice_clone", file_name_without_ext)

    sf.write(output_filename, wavs[0], sr)
    print(f"✅ 완료: {output_filename}")

# -----------------------------------------------------------------------------
# [메인 로직]
# -----------------------------------------------------------------------------

def print_help():
    print("""
[사용법] python tts.py [모드번호] [인자...]

1. Custom Voice (프리셋)
   사용법: python tts.py 1 "변환할 텍스트" [프리셋이름 (기본값: Sohee)]
   예시:   python tts.py 1 "안녕하세요" Aiden

2. Voice Design (목소리 묘사)
   사용법: python tts.py 2 "변환할 텍스트" "목소리 묘사"
   예시:   python tts.py 2 "안녕하세요" "귀여운 한국인 여자아이 목소리"

3. Voice Clone (목소리 복제)
   사용법: python tts.py 3 "변환할 텍스트" "목소리 파일 경로"
   예시:   python tts.py 3 "안녕하세요" "./my_voice.wav"

* 인자 없이 실행 시 대화형 모드로 실행됩니다.
""")

def main():
    args = sys.argv[1:]
    
    # 1. 인자가 없는 경우 -> 대화형 모드
    if len(args) == 0:
        print("\n=== Qwen3 TTS 대화형 모드 ===")
        print("1. Custom Voice (프리셋 선택)")
        print("2. Voice Design (목소리 묘사)")
        print("3. Voice Clone  (목소리 복제)")
        
        mode = input("\n원하는 모드를 선택하세요 (1/2/3): ").strip()
        
        if mode == "1":
            t = input("변환할 텍스트: ").strip()
            s = input("원하는 프리셋 (기본값 Sohee): ").strip()
            if not s: s = "Sohee"
            run_custom_voice(t, s)
            
        elif mode == "2":
            t = input("변환할 텍스트: ").strip()
            i = input("원하는 목소리 묘사: ").strip()
            run_voice_design(t, i)
            
        elif mode == "3":
            t = input("변환할 텍스트: ").strip()
            p = input("참조 오디오 경로: ").strip()
            # 대화형에서는 명시적으로 받음
            r = input("참조 오디오의 텍스트 내용: ").strip()
            run_voice_clone(t, p, r)
            
        else:
            print("잘못된 입력입니다.")
            
    # 2. 인자가 있는 경우 -> CLI 모드
    else:
        mode = args[0]
        
        if mode == "1":
            # python tts.py 1 "text" "speaker"
            if len(args) < 2:
                print("❌ 텍스트 인자가 필요합니다.")
                print_help()
                return
            
            text = args[1]
            speaker = args[2] if len(args) > 2 else "Sohee"
            run_custom_voice(text, speaker)
            
        elif mode == "2":
            # python tts.py 2 "text" "instruct"
            if len(args) < 3:
                print("❌ 텍스트와 묘사 인자가 필요합니다.")
                print_help()
                return
                
            text = args[1]
            instruct = args[2]
            run_voice_design(text, instruct)
            
        elif mode == "3":
            # python tts.py 3 "text" "path"
            if len(args) < 3:
                print("❌ 텍스트와 파일 경로 인자가 필요합니다.")
                print_help()
                return
                
            text = args[1]
            path = args[2]
            # CLI 모드에서는 ref_text를 인자로 받지 않기로 했으므로 내부에서 처리(None 전달)
            run_voice_clone(text, path, ref_text=None)
            
        else:
            print_help()

if __name__ == "__main__":
    main()
